from .monthly_payment_calc import MonthlyPaymentCalc
import math
import numpy as np
import pandas as pd


class StudentLoan(object):

    def __init__(self, loan: float, intRate: float, payment: float, years:int) -> None:
        """The constructor.

        Keyword arguments:
        loan -- student loan amount (default 1000)
        intRate -- interest rate (default 0.001)
        payment -- monthly payment amount (default 100)
        years -- years to repay loan (default 1)
        """
        self.__loan = loan
        self.__intRate = intRate
        self.__years = years
        self.__payment = payment
        self.__paymentCalc = MonthlyPaymentCalc()

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
        return self.__paymentCalc.calculate(self.__loan, self.__intRate, self.__years)
    
    
    # List of variable names in the methods below:
    #
    # pb -- Principal Balance
    # intPaid -- Interest Paid
    # prinPaid -- Principal Paid
    # nb -- New Balance

    def getRepayTime(self) -> str:
        """Return time it will take to repay loan"""
        nb = self.__loan
        lastMonth = self.__years * 12
        for i in range(lastMonth):
            if nb > 0:
                month = i + 1
                pb = nb
                nb = self.__getNewBalance(pb)
        if month == lastMonth and nb > 0:
            payIncr = self.__getIncreasePay()
            return payIncr
        else:
            payDet = self.__getPayDetails(month)
            return payDet

    # NumPy and Pandas is used in the getSchedule() method
    # below to create a data frame. The created data frame
    # is an amortization schedule.
    def getSchedule(self) -> pd.DataFrame:
        """Return loan amortization schedule"""
        pd.set_option('max_rows', 360)
        nb = self.__loan
        payment = self.__payment
        scheduleData = []
        lastMonth = self.__years * 12
        for i in range(lastMonth):
            dataRow = []
            if nb <= 0:
                break
            else:
                month = i + 1
                pb = nb
                intPaid = self.__intRate / 12 * pb
                prinPaid = self.__payment - intPaid
                if prinPaid > pb:
                    prinPaid = pb
                    payment = intPaid + prinPaid
                nb = pb - prinPaid
                dataRow.append(month)
                dataRow.append(f'${pb:,.2f}')
                dataRow.append(f'${payment:,.2f}')
                dataRow.append(f'${intPaid:,.2f}')
                dataRow.append(f'${prinPaid:,.2f}')
                if nb > 0:
                    dataRow.append(f'${nb:,.2f}')
                else:
                    dataRow.append('$0.00')
                scheduleData.append(dataRow)

        # np -- NumPy
        # pd -- Pandas
        userData = np.array(scheduleData)
        column_names = ['Month', 'Principal Balance', 'Payment',
                        'Interest Paid', 'Principal Paid', 'New Balance']
        df = pd.DataFrame(data=userData, columns=column_names)
        return df

    # Private Method
    def __getNewBalance(self, pb: float) -> float:
        """Return new principal balance of loan after making a payment.

        Keyword arguments:
        pb -- principal balance
        """
        intPaid = self.__intRate / 12 * pb
        prinPaid = self.__payment - intPaid
        nb = pb - prinPaid
        return nb

    # Private Method
    def __getPayDetails(self, month: int) -> str:
        """Return details of payment duration.

        Keyword arguements:
        month -- number of months it will take to repay loan
        """
        return f"""The ${self.__loan:,.2f} loan will take {math.floor(month / 12)} years 
                and {month % 12} months to repay with an increased monthly payment 
                of ${self.__payment:,.2f}."""

    # Private Method
    def __getIncreasePay(self) -> str:
        """Return suggestion to increase monthly payment"""
        mPay = self.__getMonPayment(self.__loan, self.__intRate, self.__years)
        word = 'year'
        if self.__years > 1:
            word = word + 's'
        return f"""The ${self.__loan:,.2f} loan will take over {self.__years} years to repay
                with a monthly payment of ${self.__payment:,.2f}. \n\nIncrease monthly payment 
                to ${mPay:,.2f} to repay the loan within {self.__years} {word}."""

    # Private Method
    def __getMonPayment(self, loan: float, intRate: float, years: int) -> float:
        """Return monthly payment amount.

        Keyword arguments:
        loan -- laon amount
        intRate -- interest rate
        years -- years to repay loan
        """
        return self.__paymentCalc.calculate(loan, intRate, years)

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
