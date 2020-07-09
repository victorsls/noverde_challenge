import uuid
from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Loan(models.Model):
    PROCESSING, COMPLETED = 'processing', 'completed'
    STATUS_CHOICES = ((PROCESSING, PROCESSING), (COMPLETED, COMPLETED))

    APPROVED, REFUSED = 'approved', 'refused'
    RESULT_CHOICES = ((APPROVED, APPROVED), (REFUSED, REFUSED))

    AGE, SCORE, COMMITMENT = 'age', 'score', 'commitment'
    REFUSED_POLICY_CHOICES = ((AGE, AGE), (SCORE, SCORE), (COMMITMENT, COMMITMENT))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    amount = models.DecimalField(
        validators=[MinValueValidator(1000), MaxValueValidator(5000)], decimal_places=2, max_digits=6
    )
    score = models.IntegerField(null=True)
    terms = models.IntegerField()
    income = models.DecimalField(decimal_places=2, max_digits=6)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, null=True)
    result = models.CharField(choices=RESULT_CHOICES, max_length=10, null=True)
    refused_policy = models.CharField(choices=REFUSED_POLICY_CHOICES, max_length=10, null=True)

    def __str__(self):
        return f'{self.name} - {self.cpf}'

    def calculate_age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Meta:
        db_table = 'loan'


@receiver(post_save, sender=Loan)
def check_policies(sender, instance, created, **kwargs):
    from challenge.loan.tasks import age_policy, score_policy, commitment_policy
    if created:
        age_policy.delay(loan_id=instance.id)
    elif instance.status == instance.PROCESSING and not instance.score:
        score_policy.delay(loan_id=instance.id)
    elif instance.status == instance.PROCESSING and instance.score:
        commitment_policy.delay(loan_id=instance.id)
