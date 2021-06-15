$(document).ready(function() {
    $("#btnCalculate").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val(),
            interestRate: $("#txtInterestRate").val(),
            yearsToRepay: $("#txtYearsToRepay").val()
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result);
            $("#scheduleViewButton").html('<button id="btnSchedule">View Amortization Schedule<\/button>');
            document.getElementById("scheduleTable").innerHTML = data.schedule;
        });
        return false;
    });
});