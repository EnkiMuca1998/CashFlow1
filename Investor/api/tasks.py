import pandas as pd
from pyxirr import xirr
from celery import shared_task
from Investor.models import CashFlow, Loan
import os

@shared_task
def read_line(x, y) :
    loan = pd.read_csv(x)
    cashflow = pd.read_csv(y)

    # Create new cashflow
    for index, row in cashflow.iterrows():
        try:
            CashFlow.objects.create(
            loan_identifier=row['loan_identifier'],
            reference_date=row['reference_date'],
            type=row['type'],
            amount=row['amount'], )
        except:
            pass

    # Create new loan
    for index, row in loan.iterrows():
        try:
            Loan.objects.get(identifier=row['identifier'])
        except:
            funding_reference_date = CashFlow.objects.get(loan_identifier=row['identifier'], type='Funding').reference_date

            try :
                repayment_reference_date = CashFlow.objects.get(loan_identifier=row['identifier'], type='Repayment').reference_date
            except :
                pass
            sum_funding = sum(CashFlow.objects.filter(loan_identifier=row['identifier'], type='Funding').values_list('amount',flat=True))
            invested_amount = abs(sum_funding)
            sum_repayment = sum(CashFlow.objects.filter(loan_identifier=row['identifier'], type='Repayment').values_list('amount',flat=True))

            #Expected IRR
            dates = [funding_reference_date, row['maturity_date']]
            amounts = [sum_funding, invested_amount + row['total_expected_interest_amount'] * (invested_amount / row['total_amount'])]
            xirr(dates, amounts)
            xirr(zip(dates, amounts))

            #Realized IRR
            if sum_repayment >= (invested_amount + (row['total_expected_interest_amount'] * (invested_amount / row['total_amount']))):
                dates2 = [funding_reference_date, repayment_reference_date]
                amounts2 = [sum_funding, sum_repayment]
                xirr(dates2, amounts2)
                xirr(zip(dates2, amounts2))

            #Create new loan
            Loan.objects.create(
                identifier=row['identifier'],
                issue_date=row['issue_date'],
                total_amount=row['total_amount'],
                rating=row['rating'],
                maturity_date=row['maturity_date'],
                total_expected_interest_amount=row['total_expected_interest_amount'],
                invested_amount=invested_amount,
                investment_date=funding_reference_date,
                expected_interest_amount=row['total_expected_interest_amount'] * (invested_amount / row['total_amount']),
                is_closed=1 if sum_repayment >= (invested_amount + (row['total_expected_interest_amount'] * (invested_amount / row['total_amount'])))
                else 0,
                expected_irr=xirr(pd.DataFrame({"dates": dates, "amounts": amounts})),
                realized_irr=xirr(pd.DataFrame({"dates": dates2, "amounts": amounts2})) if sum_repayment >= (invested_amount + (row['total_expected_interest_amount'] * (invested_amount / row['total_amount'])))
                else 0)
    #Delete file system storage
    os.remove(x)
    os.remove(y)


