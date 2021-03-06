import numpy as np
import pandas as pd


class AmortizationSchedule:

    def __init__(self, loan: float, intRate: float, payment: float, years:int) -> None:
        """The constructor.

        Args:
            loan: loan amount
            intRate: interest rate
            payment: monthly payment amount
            years: years to repay loan
        """
        if loan <= 0:
            raise ValueError("A loan amount must be greater than 0.")
        elif intRate <= 0:
            raise ValueError("A loan's interest rate must be greater than 0.")
        elif years <= 0:
            raise ValueError("A loan's repayment period must be greater than 0 years.")
        elif payment <=0:
            raise ValueError("A loan payment must be greater than 0.")
        self.__loan = loan
        self.__intRate = intRate
        self.__payment = payment
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
    
    def setPayment(self, value: float) -> None:
        self.__payment = value
    
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
        return self.__payment


    # NumPy and Pandas is used in the getSchedule() method
    # below to create a data frame. The created data frame
    # is an amortization schedule.
    def getSchedule(self) -> pd.DataFrame:
        """Returns the amortization schedule of a loan"""
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