
# The LoanX tool is designed on Google Colab.


##################################################################
# MARKDOWN + CODE INSIDE "Calculate Monthly Payment" CELL

#@title << Calculate Monthly Payment
# double click the form on the right to hide code  -->

Loan_Amount =   0#@param {type:"number"}
Interest_Rate =   0#@param {type:"number"}
Years_to_Repay =   0#@param {type:"number"}


# LoanX uses the Python libaries NumPy and Pandas. These two
# powerful libraries are popularly used for data analysis and 
# visualization. The libraries are implemented in the code 
# for the StudentLoan class.

import numpy as np
import pandas as pd
import math
from google.colab import files


# FUNCTIONS

def numsValid(lst):
    """Return True if all numbers in the list are greater than 0.
    Returns False otherwise.

    Checks if user inputs are valid numbers greater than 0
    Return boolean (true or false)

    KeyWord arguments:
    lst -- list of numbers
    
    """
    for nums in lst:
        if nums <= 0:
            return False
        else:
            try:
                float(nums)
            except:
                return False
    return True


def monPayment(loan, intRate, years):
    """Return monthly payment amount.

    1. Calculate the monthly payment amount of a student loan 
       in the LoanX forms.
    2. Parse calculation to round number to 2 decimal places
    3. Return monthly payment amount

    Keyword arguments:
    loan -- laon amount
    intRate -- interest rate
    years -- years to repay loan
    """
    j = intRate / 12
    n = years * 12
    monPay = loan * (j / (1 - (1 + j)**-n))
    strMonPay = str(monPay)
    if '.' in strMonPay:
        strMonPay = strMonPay.split('.') # parse string to get first 2 numbers after decimal 
        r = strMonPay[1]
        if len(r) > 2:
            r = int(r[:2]) + 1 
        elif len(r) == 1:
            r = int(r + '0')
        else:
            r = int(r[:2])
        monPay = math.floor(monPay) + (r / 100)
    return f'${monPay:,.2f}'


def checkRate(intRate):
    """Check if interest rate is decimal or percentage.

    Interest rates can be entered on the LoanX forms as a 
    decimal or percent value. LoanX will assume the interest
    rate is less than 100%.

    Keyword arguments:
    intRate -- interest rate
    """
    if intRate >= 1:
        intRate = intRate / 100
    return intRate


def download(dataFrame):
    """Download Pandas dataframe as a CSV file.

    Keyword arguments:
    dataFrame -- Pandas data frame
    """
    df = dataFrame
    df.to_csv('amortization_schedule.csv')
    files.download('amortization_schedule.csv')


# StudentLoan CLASS
#
# The code below creates a StudentLoan class
#
# Keyword arguments:
#       loan -- student loan amount (default 1000)
#       intRate -- interest rate (default 0.001)
#       payment -- monthly payment amount (default 100)
#       years -- years to repay loan (default 1)
#
# Methods:
#       1. setLoan() -- set the loan amount
#       2. setIntRate() -- set the interest rate
#       3. setPayment() -- set the monthly payment amount
#       4. setYears() -- set the number of years to repay the loan
#       5. repay() -- return the time it will take to repay loan
#       6. schedule() -- return loan amortazion schedule

class StudentLoan(object):

    def __init__(self, loan=1000, intRate=0.001,
                 payment=100, years=1):
        """The constructor"""
        self.loan = loan
        self.intRate = intRate
        self.payment = payment
        self.years = years

    def setLoan(self, value):
        """Set the loan amount"""
        self.loan = value

    def setIntRate(self, value):
        """Set the interest rate"""
        self.intRate = value

    def setPayment(self, value):
        """Set the monthly payment amount"""
        self.payment = value

    def setYears(self, value):
        """Set the number of years to repay the loan"""
        self.years = value

    # List of variable names in the methods below:
    #
    # pb -- Principal Balance
    # intPaid -- Interest Paid
    # prinPaid -- Principal Paid
    # nb -- New Balance

    def repay(self):
        """Return time it will take to repay loan"""
        nb = self.loan
        lastMonth = self.years * 12
        for i in range(lastMonth):
            if nb > 0:
                month = i + 1
                pb = nb
                nb = self.__newBal(pb)
        if month == lastMonth and nb > 0:
            payIncr = self.__payIncrease()
            return payIncr
        else:
            payDet = self.__payDetails(month)
            return payDet
            

    # NumPy and Pandas is used in the schedule() method
    # below to create a data frame. The created data frame
    # is an amortization schedule. 
    
    def schedule(self):
        """Return loan amortization schedule"""
        pd.set_option('max_rows', 360)
        nb = self.loan
        payment = self.payment
        scheduleData = []
        lastMonth = self.years * 12
        for i in range(lastMonth):
            dataRow = []
            if nb <= 0:
                break
            else:
                month = i + 1
                pb = nb
                intPaid = self.intRate / 12 * pb
                prinPaid = self.payment - intPaid
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
        column_names = ['Month', 'Principal_Balance', 'Payment', 'Interest_Paid', 'Principal_Paid', 'New_Balance']
        df = pd.DataFrame(data=userData, columns=column_names)
        df.set_index('Month', inplace=True)
        return df

    # Private Method
    def __newBal(self, pb):
        """Return new principal balance of loan after making a payment.

        Keyword arguments:
        pb -- principal balance
        """
        intPaid = self.intRate / 12 * pb
        prinPaid = self.payment - intPaid
        nb = pb - prinPaid
        return nb

    # Private Method
    def __payDetails(self, month):
        """Return details of payment duration.

        Keyword arguements:
        month -- number of months it will take to repay loan
        """
        return f'''The ${self.loan:,.2f} loan will take {math.floor(month / 12)} years 
        and {month % 12} months to repay with a monthly payment of ${self.payment:,.2f}.'''

    # Private Method
    def __payIncrease(self):
        """Return suggestion to increase monthly payment"""
        mPay = self.__monPayment(self.loan, self.intRate, self.years)
        word = 'year'
        if self.years > 1:
            word = word + 's'
        return f'''The ${self.loan:,.2f} loan will take over {self.years} years to repay
        with a monthly payment of ${self.payment:,.2f}. \n\nIncrease monthly payment to
        ${mPay:,.2f} to repay the loan within {self.years} {word}.'''
        
    # Private Method
    def __monPayment(self, loan, intRate, years):
        """Return monthly payment amount.

        Keyword arguments:
        loan -- laon amount
        intRate -- interest rate
        years -- years to repay loan
        """
        j = intRate / 12
        n = years * 12
        monPay = loan * (j / (1 - (1 + j)**-n))
        strMonPay = str(monPay)
        if '.' in strMonPay:
            strMonPay = strMonPay.split('.')
            r = strMonPay[1]
            if len(r) > 2:
                r = int(r[:2]) + 1
            elif len(r) == 1:
                r = int(r + '0')
            else:
                r = int(r[:2])
            return math.floor(monPay) + (r / 100)
        return monPay

    def __repr__(self):
        """Representation of StudentLoan object"""
        print(f'StudentLoan({self.loan}, {self.intRate}, {self.payment}, {self.years})')

    def __str__(self):
        """String representation of StudentLoan object"""
        word = 'year'
        if self.years > 1:
            word = word + 's'
        print(f'''The ${self.loan:,.2f} student loan has an interest rate 
        of {self.intRate * 100:.2f}% and monthly payment of ${self.payment:,.2f}.''')
        print()
        print(f'The loan must be repaid within {self.years} {word}.')





# Python code for "Calculate Monthly Payment" FORM
# 1. Check if inputs are valid numbers 
# 2. Check if interest rate input is decimal or percent
# 3. Calculate monthly payment
# 4. Handle exceptions
    
try:
    valid = numsValid([Loan_Amount, Interest_Rate, Years_to_Repay])
    if valid:
        Interest_Rate = checkRate(Interest_Rate)
        payment = monPayment(Loan_Amount, Interest_Rate, Years_to_Repay)
        print(payment)
    else:
        print('All values must be a number greater than 0')
except:
    print('Sorry, we couldn\'t process your request.')
    print()
    print('''Please double check that you pressed play on all previous cells
    at least once.''')




##################################################################
# MARKDOWN + CODE INSIDE "Create Amortization Schedule" CELL


#@title << Create Amortization Schedule
# double click the form on the right to hide code  -->
#@markdown Note: You may have to scroll up a created schedule to view "Month 1."

#@title Number fields
Loan_Amount =   0#@param {type:"number"}
Interest_Rate =   0#@param {type:"number"}
Years_to_Repay =   0#@param {type:"number"}
Monthly_Payment =   0#@param {type:"number"}


# Python code for "Create Amortization Schedule" FORM
# 1. Check if inputs are valid numbers 
# 2. Check if interest rate input is decimal or percent
# 3. Creates a StudentLoan object
# 4. Call and print repay() method
# 5. Display loan amortization schedule
# 6. Handle exceptions

try:
    valid = numsValid([Loan_Amount, Interest_Rate, Monthly_Payment, Years_to_Repay])
    if valid:
        Interest_Rate = checkRate(Interest_Rate)
        a = StudentLoan(Loan_Amount, Interest_Rate, Monthly_Payment, Years_to_Repay)
        details = a.repay()
        if "Increase" in details:
          print(details)
        else:
          print(details)
          print()
          display(a.schedule())
    else:
        print('All values must be a number greater than 0')
        print()
except:
    print('Sorry, we couldn\'t process your request.')
    print()
    print('''Please double check that you pressed play on all previous cells
    at least once.''')




##################################################################
# MARKDOWN + CODE INSIDE "Download Amortization Schedule" CELL

#@title << Download Amortization Schedule
# double click the empty area on the right to hide code  -->


# Python code for Downloading CSV file
# 1. Call the download() function
# 2. Hanlde exceptions

try:
    download(a.schedule())
except:
    print('Sorry, we couldn\'t process your request.')
    print()
    print('''Please double check that you pressed play on all previous cells
    at least once.''')
