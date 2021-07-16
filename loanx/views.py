import os
from loanx.loan.amort_schedule import AmortizationSchedule
from loanx import app
from .loan.studentloan import StudentLoan
from .explore_feature.extra_pay_schedule import ExtraPaymentSchedule
from flask import jsonify, render_template, request, url_for


@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page of the website"""
    return render_template('index.html')


@app.route('/get_monthly_payment', methods=['GET', 'POST'])
def get_monthly_payment():
    """Returns a loan's monthly payment amount and amortization schedule in JSON format"""
    loanAmount = request.args.get('loanAmount', 0, type=float)
    interestRate = request.args.get('interestRate', 0, type=float) / 100
    yearsToRepay = request.args.get('yearsToRepay', 0, type=int)

    studentLoan = StudentLoan(loanAmount, interestRate, yearsToRepay)
    payment = studentLoan.getPayment()
    loanSchedule = studentLoan.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    return jsonify(result=f'{payment:,.2f}', schedule=loanSchedule)  # format payment to include a comma


@app.route('/get_explore_payment', methods=['GET', 'POST'])
def get_explore_payment():
    """Returns a loan's monthly payment amount, amortization schedule, payoff details, 
        and increased payment amount in JSON format.
    """
    loanAmount = request.args.get('loanAmount', 0, type=float)
    interestRate = request.args.get('interestRate', 0, type=float) / 100
    yearsToRepay = request.args.get('yearsToRepay', 0, type=int)
    extraPayment = request.args.get('extraPayment', 0, type=float)

    studentLoan = StudentLoan(loanAmount, interestRate, yearsToRepay)
    payment = studentLoan.getPayment()
    increasedPayment = payment + extraPayment
    extraPaySchedule = ExtraPaymentSchedule(loanAmount, interestRate, increasedPayment, yearsToRepay)
    loanSchedule = extraPaySchedule.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    earlyPayoff = extraPaySchedule.getRepayTime().lower()
    return jsonify(result=f'{increasedPayment:,.2f}', schedule=loanSchedule, details=earlyPayoff, originalPayment=f'{payment:,.2f}')


@app.errorhandler(404)
def page_not_found(error):
    """Renders a webpage dedicated to 404 Page Not Found Error"""
    return render_template('page_not_found.html'), 404