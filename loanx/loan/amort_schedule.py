import numpy as np
import pandas as pd
from .studentloan import StudentLoan


class AmortizationSchedule:

    def __init__(self, loan: StudentLoan) -> None:
        """The constructor.

        Args:
            loan: student loan object
        """
        self.__loan = loan
    
    def getLoanAmount(self) -> float:
        """Returns the loan amount"""
        return self.__loan.getLoanAmount()

    def getInterestRate(self) -> float:
        """Returns the interest rate"""
        return self.__loan.getInterestRate()
    
    def getYears(self) -> int:
        """Returns the number of years to repay the loan"""
        return self.__loan.getYears()
    
    def getPayment(self) -> float:
        """Returns the monthly payment amount"""
        return self.__loan.getPayment()

    # List of variable names in the methods below:
    #
    # pb -- Principal Balance
    # intPaid -- Interest Paid
    # prinPaid -- Principal Paid
    # nb -- New Balance

    def getSchedule(self) -> pd.DataFrame:
        """Returns the amortization schedule of a loan.
        
        NumPy and Pandas is used in this method to
        create a data frame. The created data frame
        is an amortization schedule.
        """
        pd.set_option('max_rows', 360)
        nb = self.getLoanAmount()
        payment = self.getPayment()
        scheduleData = []
        lastMonth = self.getYears() * 12
        for i in range(lastMonth):
            dataRow = []
            if nb <= 0:
                break
            else:
                month = i + 1
                pb = nb
                intPaid = self.getInterestRate() / 12 * pb
                prinPaid = self.getPayment() - intPaid
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