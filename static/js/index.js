$(document).ready(function() {
    $("#btnSubmit").bind('click', function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val(),
            interestRate: $("#txtInterestRate").val(),
            yearsToRepay: $("#txtYearsToRepay").val()
        }, function(data) {
            $("#monthlyPayment").text(data.result);
            console.log(data.result)
        });
        return false;
    });
});