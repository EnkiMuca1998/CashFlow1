from django.db import models

class Loan(models.Model):

    identifier = models.CharField(null=True, blank=True, max_length=150)
    issue_date = models.DateField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    total_expected_interest_amount = models.FloatField(null=True, blank=True)
    invested_amount = models.FloatField(null=True, blank=True)
    investment_date = models.DateField(null=True, blank=True)
    expected_interest_amount = models.FloatField(null=True, blank=True)
    is_closed = models.BooleanField(null=True, blank=True, default=False)
    expected_irr = models.FloatField(null=True, blank=True)
    realized_irr = models.FloatField(null=True, blank=True)


class CashFlow(models.Model):

    loan_identifier = models.CharField(null=True, blank=True, max_length=150)
    reference_date = models.DateField(null=True, blank=True)
    type = models.CharField(null=True, blank=True, max_length=150)
    amount = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['type', 'loan_identifier', 'amount', 'reference_date']


