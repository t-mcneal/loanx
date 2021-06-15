$(document).ready(function() {
    $("#btnCalculate").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val(),
            interestRate: $("#txtInterestRate").val(),
            yearsToRepay: $("#txtYearsToRepay").val()
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result);
            $("#scheduleViewButton").html('<button id="btnSchedule" onclick="viewSchedule();">View Amortization Schedule<\/button>');
            document.getElementById("scheduleTable").innerHTML = data.schedule;
        });
        return false;
    });
});



function viewSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "inline-block";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="hideSchedule();">Hide Amortization Schedule<\/button>'
}

function hideSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "none";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="viewSchedule();">View Amortization Schedule<\/button>'

}

