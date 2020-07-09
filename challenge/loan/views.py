from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet

from challenge.loan.models import Loan
from challenge.loan.serializers import CreateLoanSerializer


class CreateLoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = CreateLoanSerializer
    http_method_names = ['post', 'get']

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")
