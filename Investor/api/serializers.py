from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from Investor.models import Loan, CashFlow
from Investor.api.tasks import read_line

class csvFileSerializer(serializers.Serializer):

    loan = serializers.FileField()
    cashflow = serializers.FileField()

    def create(self, validated_data):
        loan1 = validated_data['loan']
        cashflow1 = validated_data['cashflow']
        storage = FileSystemStorage()
        storage.save(loan1.name, loan1)
        storage.save(cashflow1.name, cashflow1)
        return read_line.delay(x=storage.path(loan1.name), y=storage.path(cashflow1.name))


class ImportDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = "__all__"


class ImportDataSerializer1(serializers.ModelSerializer):

    class Meta:
        model = CashFlow
        fields = "__all__"