from loanx import app
from .loan.studentloan import StudentLoan
from .loan.monthly_payment_calc import MonthlyPaymentCalc
from flask import jsonify, render_template, request


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/get_monthly_payment', methods=['GET', 'POST'])
def get_monthly_payment():
    loanAmount = request.args.get('loanAmount', 0, type=float)
    interestRate = request.args.get('interestRate', 0, type=float) / 100
    yearsToRepay = request.args.get('yearsToRepay', 0, type=int)
    payment = MonthlyPaymentCalc.calculate(loanAmount, interestRate, yearsToRepay)
    studentLoan = StudentLoan(loanAmount, interestRate, payment, yearsToRepay)
    loanSchedule = studentLoan.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    return jsonify(result=f'{payment:,.2f}', schedule=loanSchedule)  # format payment to include a comma


@app.route('/get_explore_payment', methods=['GET', 'POST'])
def get_explore_payment():
    loanAmount = request.args.get('loanAmount', 0, type=float)
    interestRate = request.args.get('interestRate', 0, type=float) / 100
    yearsToRepay = request.args.get('yearsToRepay', 0, type=int)
    extraPayment = request.args.get('extraPayment', 0, type=float)
    payment = MonthlyPaymentCalc.calculate(loanAmount, interestRate, yearsToRepay)
    increasedPayment = payment + extraPayment
    studentLoan = StudentLoan(loanAmount, interestRate, increasedPayment, yearsToRepay)
    loanSchedule = studentLoan.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    earlyPayoff = studentLoan.getRepayTime().lower()
    return jsonify(result=f'{increasedPayment:,.2f}', schedule=loanSchedule, details=earlyPayoff, originalPayment=f'{payment:,.2f}')
