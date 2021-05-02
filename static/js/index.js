$(document).ready(function() {
    $("#btnSubmit").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val(),
            interestRate: $("#txtInterestRate").val(),
            yearsToRepay: $("#txtYearsToRepay").val()
        }, function(data) {
            $("#monthlyPayment").html("<h>Your monthly payment is</h><p>$" 
            + data.result + "<p>");
        });
        return false;
    });
});