from .monthly_payment_calc import MonthlyPaymentCalc
from .amort_schedule import AmortizationSchedule
import pandas as pd


class StudentLoan:

    def __init__(self, loan: float, intRate: float, years:int) -> None:
        """The constructor.

        Args:
            loan: student loan amount
            intRate: interest rate
            years: years to repay loan
        """
        if loan <= 0:
            raise ValueError("A loan amount must be greater than 0.")
        elif intRate <= 0:
            raise ValueError("A loan's interest rate must be greater than 0.")
        elif years <= 0:
            raise ValueError("A loan's repayment period must be greater than 0 years.")
        self.__loan = loan
        self.__intRate = intRate
        self.__years = years

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
        """Returns the loan amount"""
        return self.__loan

    def getIntRate(self) -> float:
        """Returns the interest rate"""
        return self.__intRate
    
    def getYears(self) -> int:
        """Returns the number of years to repay the loan"""
        return self.__years
    
    def getPayment(self) -> float:
        """Returns the monthly payment amount"""
        return MonthlyPaymentCalc.calculate(self.__loan, self.__intRate, self.__years)

    def getSchedule(self) -> pd.DataFrame:
        """Returns the loan's amortization schedule.
        
        An amortization schedule object is instantiated in this method, instead of 
        the constructor, to future-proof the returned schedule data in case the student 
        loan class' setter methods are used.
        """
        amortSchedule = AmortizationSchedule(self.__loan, self.__intRate, self.getPayment(), self.__years) 
        return amortSchedule.getSchedule()

    def __repr__(self) -> None:
        """Representation of StudentLoan object"""
        print(f'StudentLoan({self.__loan}, {self.__intRate}, {self.getPayment()}, {self.__years})')

    def __str__(self) -> None:
        """String representation of StudentLoan object"""
        word = 'year'
        if self.__years > 1:
            word = word + 's'
        print(f"""The ${self.__loan:,.2f} student loan has an interest rate 
                of {self.__intRate * 100:.2f}% and monthly payment of ${self.getPayment():,.2f}.""")
        print()
        print(f'The loan must be repaid within {self.__years} {word}.')
