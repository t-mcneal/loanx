from .monthly_payment_calc import MonthlyPaymentCalc
from .amort_schedule import AmortizationSchedule
import pandas as pd


class StudentLoan:

    def __init__(self, loan: float, intRate: float, years:int) -> None:
        """The constructor.

        Keyword arguments:
        loan -- student loan amount
        intRate -- interest rate
        years -- years to repay loan
        """
        self.__loan = loan
        self.__intRate = intRate
        self.__years = years
        self.__payment = MonthlyPaymentCalc.calculate(self.__loan, self.__intRate, self.__years)
        self.__amortSchedule = AmortizationSchedule(loan, intRate, self.__payment, years)

    def setLoan(self, value: float) -> None:
        """Set the loan amount"""
        self.__loan = value

    def setIntRate(self, value: float) -> None:
        """Set the interest rate"""
        self.__intRate = value

    def setYears(self, value: int) -> None:
        """Set the number of years to repay the loan"""
        self.__years = value
    
    def getLoan(self) -> float:
        """Get the loan amount"""
        return self.__loan

    def getIntRate(self) -> float:
        """Get the interest rate"""
        return self.__intRate
    
    def getYears(self) -> int:
        """Get the number of years to repay the loan"""
        return self.__years
    
    def getPayment(self) -> float:
        """Get the monthly payment amount"""
        return self.__payment

    def getSchedule(self) -> pd.DataFrame:
        """Return loan amortization schedule"""
        return self.__amortSchedule.getSchedule()

    def __repr__(self) -> None:
        """Representation of StudentLoan object"""
        print(f'StudentLoan({self.__loan}, {self.__intRate}, {self.__payment}, {self.__years})')

    def __str__(self) -> None:
        """String representation of StudentLoan object"""
        word = 'year'
        if self.__years > 1:
            word = word + 's'
        print(f"""The ${self.__loan:,.2f} student loan has an interest rate 
                of {self.__intRate * 100:.2f}% and monthly payment of ${self.__payment:,.2f}.""")
        print()
        print(f'The loan must be repaid within {self.__years} {word}.')
