import json
from decimal import Decimal

import requests
from django.conf import settings
from django.core.serializers import serialize
from rest_framework import status

from challenge.celery import app
from challenge.loan.models import Loan


@app.task(name="age_policy_task")
def age_policy(loan_id, lowest_acceptable_age=18):
    loan = Loan.objects.get(id=loan_id)
    loan.status = loan.PROCESSING
    if loan.calculate_age() < lowest_acceptable_age:
        loan.status = loan.COMPLETED
        loan.result = loan.REFUSED
        loan.refused_policy = loan.AGE
    loan.save()
    return serialize('json', [loan])


@app.task(name="score_policy_task")
def score_policy(loan_id, lowest_acceptable_score=600):
    loan = Loan.objects.get(id=loan_id)
    url = f'{settings.NOVERDE_API_URL}/score'

    payload = {'cpf': loan.cpf}
    headers = {
        'x-api-key': settings.NOVERDE_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

    if response.status_code == status.HTTP_200_OK:
        score = response.json().get('score')
        loan.score = score

        if score < lowest_acceptable_score:
            loan.status = loan.COMPLETED
            loan.result = loan.REFUSED
            loan.refused_policy = loan.SCORE
    loan.save()
    return serialize('json', [loan])


@app.task(name="commitment_policy_task")
def commitment_policy(loan_id):
    loan = Loan.objects.get(id=loan_id)
    url = f'{settings.NOVERDE_API_URL}/commitment'

    payload = {'cpf': loan.cpf}
    headers = {
        'x-api-key': settings.NOVERDE_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

    if response.status_code == status.HTTP_200_OK:
        remaining_income = loan.income - (loan.income * Decimal(response.json().get('commitment')))
        terms = loan.terms
        while terms <= 12:
            installment_value = calculation_installments(loan, terms)
            if installment_value <= remaining_income:
                loan.status = loan.COMPLETED
                loan.result = loan.APPROVED
                loan.terms = terms
                break
            terms += 3
        if loan.status != loan.COMPLETED:
            loan.status = loan.COMPLETED
            loan.result = loan.REFUSED
            loan.refused_policy = loan.COMMITMENT
        loan.save()
    return serialize('json', [loan])


def get_interest_rate(score, terms):
    if score >= 900:
        data = {
            '6': 0.039,
            '9': 0.042,
            '12': 0.045
        }
    elif 800 <= score <= 899:
        data = {
            '6': 0.047,
            '9': 0.05,
            '12': 0.053
        }
    elif 700 <= score <= 799:
        data = {
            '6': 0.055,
            '9': 0.058,
            '12': 0.061
        }
    elif 600 <= score <= 699:
        data = {
            '6': 0.064,
            '9': 0.066,
            '12': 0.069
        }
    else:
        data = {}
    return Decimal(data.get(str(terms)))


def calculation_installments(loan, terms):
    interest_rate = get_interest_rate(loan.score, terms)
    return loan.amount * (
            (((1 + interest_rate) ** terms) * interest_rate) / (((1 + interest_rate) ** terms) - 1)
    )
