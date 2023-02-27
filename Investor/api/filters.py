import django_filters
from Investor.models import Loan, CashFlow

class LoanFilter(django_filters.FilterSet):

    class Meta:
        model = Loan
        fields = {
            'total_amount' : ['exact', 'gt', 'gte', 'lt', 'lte'],
            'maturity_date' : ['exact', 'year__gte', 'year__gt', 'year__lt', 'year__gte', 'year__lte'],
            'rating' : ['exact'],
            'identifier' : ['exact'],
            'total_expected_interest_amount' : ['exact', 'gt', 'gte'],
            'is_closed' : ['exact'],}


class CashFlowFilter(django_filters.FilterSet):

    class Meta:
        model = CashFlow
        fields = {
            'amount' : ['exact', 'gt', 'gte', 'lt', 'lte'],
            'reference_date' : ['exact', 'year__gte', 'year__gt', 'year__lt', 'year__gte', 'year__lte'],
            'loan_identifier' : ['exact'],
            'type' : ['exact'],}