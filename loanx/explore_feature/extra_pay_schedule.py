from loanx.loan.amort_schedule import AmortizationSchedule
from loanx.loan.monthly_payment_calc import MonthlyPaymentCalc
import math


class ExtraPaymentSchedule(AmortizationSchedule):

    def __init__(self, loan: float, intRate: float, payment: float, years:int) -> None:
        super().__init__(loan, intRate, payment, years)

    ##
    # List of variable names in the methods below:
    #
    # pb -- Principal Balance
    # intPaid -- Interest Paid
    # prinPaid -- Principal Paid
    # nb -- New Balance
    ##

    def getRepayTime(self) -> str:
        """Returns the time in years and months it will take to repay a loan"""
        nb = self.getLoan()
        lastMonth = self.getYears() * 12
        for i in range(lastMonth):
            if nb > 0:
                month = i + 1
                pb = nb
                nb = self.__getNewBalance(pb)
        if month == lastMonth and nb > 0:
            return self.__getIncreasePayDetails()
        else:
            return self.__getPayDetails(month)

    # Private Method
    def __getNewBalance(self, pb: float) -> float:
        """Returns the new principal balance of a loan after making a payment.

        Args:
            pb: principal balance
        """
        intPaid = self.getIntRate() / 12 * pb
        prinPaid = self.getPayment() - intPaid
        nb = pb - prinPaid
        return nb

    # Private Method
    def __getPayDetails(self, month: int) -> str:
        """Returns details of payment duration.

        Args:
            month: number of months it will take to repay loan
        """
        return f"""The ${self.getLoan():,.2f} loan will take {math.floor(month / 12)} years 
                and {month % 12} months to repay with an increased monthly payment 
                of ${self.getPayment():,.2f}."""

    # Private Method
    def __getIncreasePayDetails(self) -> str:
        """Returns suggestion to increase monthly payment"""
        mPay = MonthlyPaymentCalc.calculate(self.getLoan(), self.getIntRate(), self.getYears())
        word = 'year'
        if self.getYears() > 1:
            word = word + 's'
        return f"""The ${self.getLoan():,.2f} loan will take over {self.getYears()} years to repay
                with a monthly payment of ${self.getPayment():,.2f}. \n\nIncrease monthly payment 
                to ${mPay:,.2f} to repay the loan within {self.getYears()} {word}."""