from rest_framework import serializers

from challenge.loan.models import Loan


class CreateLoanSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(input_formats=['%d/%m/%Y'])

    def to_representation(self, instance):
        if not instance.status:
            data = {'id': instance.id}
        else:
            data = {
                'id': instance.id,
                'status': instance.status,
                'result': instance.result,
                'refused_policy': instance.refused_policy,
                'amount': instance.amount,
                'terms': instance.terms
            }
        return data

    class Meta:
        model = Loan
        fields = ['id', 'name', 'cpf', 'birth_date', 'amount', 'terms', 'income']
