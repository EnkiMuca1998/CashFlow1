from django.urls import path
from Investor.api.views import ImportData, NewData, FilterByLoan, FilterByCashFlow, ImportManualData



urlpatterns = [
    path('import-data/', ImportData.as_view(), name='student-detail'),
    path('import-data-manually/', ImportManualData.as_view(), name='student-detail'),
    path('statistics/', NewData.as_view(), name='student-detail'),
    path('filter-loan/', FilterByLoan.as_view(), name='student-detail'),
    path('filter-cashflow/', FilterByCashFlow.as_view(), name='student-detail'),
]