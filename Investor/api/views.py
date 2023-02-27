from Investor.api.filters import LoanFilter, CashFlowFilter
from django_filters.rest_framework import DjangoFilterBackend
from pyxirr import xirr
from rest_framework.response import Response
from rest_framework.views import APIView
from Investor.models import Loan, CashFlow
from Investor.api.serializers import csvFileSerializer, ImportDataSerializer, ImportDataSerializer1
import pandas as pd
from rest_framework import permissions as perm, generics
from user.api.permissions import IsStaffUser


class ImportData(APIView):
    permission_classes = (perm.IsAuthenticated, IsStaffUser,)
    def post(self, request, *args, **kwargs):
        serializer = csvFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG" : "SUCCESS"})
        return Response(serializer.errors)


class ImportManualData(APIView):
    permission_classes = (perm.IsAuthenticated, IsStaffUser,)
    def post(self, request, *args, **kwargs):
        serializer = ImportDataSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_CashFlow = Loan.objects.get(identifier=request.data['loan_identifier'])
            funding_amount = sum(CashFlow.objects.filter(loan_identifier=request.data['loan_identifier'], type='Funding').values_list('amount', flat=True))
            invested_amount = abs(sum(CashFlow.objects.filter(loan_identifier=request.data['loan_identifier'], type='Funding').values_list('amount', flat=True)))
            total_repayment = sum(CashFlow.objects.filter(loan_identifier=request.data['loan_identifier'], type='Repayment').values_list('amount', flat=True))

            new_CashFlow.invested_amount = invested_amount
            new_CashFlow.expected_interest_amount = new_CashFlow.total_expected_interest_amount * (new_CashFlow.invested_amount / new_CashFlow.total_amount)
            new_CashFlow.is_closed = 1 if total_repayment >= (new_CashFlow.invested_amount + new_CashFlow.expected_interest_amount) else 0
            funding_reference_date = CashFlow.objects.get(loan_identifier= request.data['loan_identifier'], type = 'Funding').reference_date

            dates = [funding_reference_date, Loan.objects.get(identifier=request.data['loan_identifier']).maturity_date]
            amounts = [funding_amount, (new_CashFlow.invested_amount + new_CashFlow.expected_interest_amount)]
            xirr(dates, amounts)
            xirr(zip(dates, amounts))
            new_CashFlow.expected_irr = xirr(pd.DataFrame({"dates": dates, "amounts": amounts}))

            dates2 = [CashFlow.objects.get(loan_identifier= request.data['loan_identifier'], type = 'Funding').reference_date, CashFlow.objects.get(loan_identifier= request.data['loan_identifier'], type = 'Repayment').reference_date]
            amounts2 = [funding_amount, total_repayment]
            xirr(dates2, amounts2)
            xirr(zip(dates2, amounts2))
            new_CashFlow.realized_irr = xirr(pd.DataFrame({"dates": dates2, "amounts": amounts2}))

            new_CashFlow.save()
            return Response(serializer.data)
        return Response(serializer.errors)




class NewData(APIView):
    permission_classes = (perm.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        sum_invested = sum(Loan.objects.all().values_list('invested_amount', flat=True))
        current_open = Loan.objects.filter(is_closed=0)
        total_repaid = sum(CashFlow.objects.filter(type='Repayment').values_list('amount', flat=True))
        a = Loan.objects.all().values_list('realized_irr', flat=True)
        b = Loan.objects.all().values_list('invested_amount', flat=True)
        res = dict(zip(b, a))
        sum1 = 0
        for key, value in res.items():
            irr = key * value / sum_invested
            sum1 = sum1 + irr
        final = {'Total Investment' : sum_invested, 'Current Loans' : current_open, 'Total Repayment' : total_repaid, 'Average Realized IRR' : sum1}
        return Response(final)


class FilterByLoan(generics.ListAPIView):
    permission_classes = (perm.IsAuthenticated,)
    queryset = Loan.objects.all()
    serializer_class = ImportDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoanFilter
    http_method_names = ['get']


class FilterByCashFlow(generics.ListAPIView):
    permission_classes = (perm.IsAuthenticated,)
    queryset = CashFlow.objects.all()
    serializer_class = ImportDataSerializer1
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowFilter
    http_method_names = ['get']