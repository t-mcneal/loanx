from loanx import app
from .loan.studentloan import StudentLoan
from .loan.amort_schedule import AmortizationSchedule
from .explore_feature.extra_pay_schedule import ExtraPaymentSchedule
from flask import jsonify, render_template, request, url_for, redirect
import os


@app.route('/')
def home():
    """Renders the homepage of the website"""
    return render_template('index.html')


@app.route('/api/v1/payment/regular', methods=['POST'])
def get_monthly_payment():
    """Returns a loan's monthly payment amount and amortization schedule in JSON format"""
    loanAmount = float(request.form['loanAmount'])
    interestRate = float(request.form['interestRate']) / 100
    yearsToRepay = int(request.form['yearsToRepay'])

    studentLoan = StudentLoan(loanAmount, interestRate, yearsToRepay)
    payment = studentLoan.getPayment()
    amortSchedule = AmortizationSchedule(studentLoan)
    scheduleHTML = amortSchedule.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    return jsonify(result=f'{payment:,.2f}', schedule=scheduleHTML)  # format payment to include a comma


@app.route('/api/v1/payment/explore', methods=['POST'])
def get_explore_payment():
    """Returns a loan's monthly payment amount, amortization schedule, payoff details, 
        and increased payment amount in JSON format.
    """
    loanAmount = float(request.form['loanAmount'])
    interestRate = float(request.form['interestRate']) / 100
    yearsToRepay = int(request.form['yearsToRepay'])
    extraPayment = float(request.form['extraPayment'])

    studentLoan = StudentLoan(loanAmount, interestRate, yearsToRepay)
    payment = studentLoan.getPayment()
    increasedPayment = payment + extraPayment
    amortSchedule = ExtraPaymentSchedule(studentLoan, extraPayment)
    scheduleHTML = amortSchedule.getSchedule().to_html(index=False, table_id='scheduleDataFrame')
    earlyPayoff = amortSchedule.getRepayTime().lower()
    return jsonify(result=f'{increasedPayment:,.2f}', schedule=scheduleHTML, details=earlyPayoff, originalPayment=f'{payment:,.2f}')


@app.errorhandler(404)
def page_not_found(error):
    """Renders a webpage dedicated to 404 Page Not Found Error"""
    return render_template('page_not_found.html'), 404


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """Adds last modified timestamp to static files.
    
    Keyword arguments:
    endpoint -- directory of files to add time stamps
    **values -- keyworded, variable-length argument list of files in the endpoint directory
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            filePath = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(filePath).st_mtime)
    return url_for(endpoint, **values)
