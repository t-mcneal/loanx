from flask import Flask, jsonify, render_template, request
import math
import numpy
import pandas

app = Flask(__name__)



@app.route('/get_monthly_payment', methods=['POST'])
def get_monthly_payment():
    if request.method == "POST":
        loanAmount = float(request.form['loanAmount'])
        interestRate = float(request.form['interestRate'])
        yearsToRepay = int(request.form['yearsToRepay'])
        payment = getMonPayment(loanAmount, interestRate, yearsToRepay)
        return render_template('index.html', result=f'{payment:.2f}')

@app.route('/')
def home():
    return render_template('index.html')


def getMonPayment(loan, intRate, years):
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
    

class StudentLoan(object):

    def __init__(self, loan=1000, intRate=0.001,
                 payment=100, years=1):
        """The constructor.
        
        Keyword arguments:
        loan -- student loan amount (default 1000)
        intRate -- interest rate (default 0.001)
        payment -- monthly payment amount (default 100)
        years -- years to repay loan (default 1)
        """
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

    # List of variables names in the methods below:
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
with a monthly payment of ${self.payment:,.2f}. \n\nIncrease monthly payment to ${mPay:,.2f} to repay the loan 
within {self.years} {word}.'''
        
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
