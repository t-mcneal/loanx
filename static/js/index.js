$(document).ready(function() {
    $("#btnCalculate").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val(),
            interestRate: $("#txtInterestRate").val(),
            yearsToRepay: $("#txtYearsToRepay").val()
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result);
            $("#scheduleViewButton").html('<button id="btnSchedule" onclick="viewSchedule();">View Amortization Schedule<\/button><p><i class="arrow up"></i></p>');
            $("#scheduleTable").html('<h2 id="scheduleHeader">Amortization Schedule<h2>' + data.schedule);
            document.getElementById("scheduleHeader").style.display = "none"; 
            document.getElementById("scheduleDataFrame").style.display = "none"; // data.schedule ID selector is scheduleDataFrame
        });
        return false;
    });
});

function viewSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "table";
    document.getElementById("scheduleHeader").style.display = "block";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="hideSchedule();">Hide Amortization Schedule<\/button><p><i class="arrow down"></i></p>'
}

function hideSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "none";
    document.getElementById("scheduleHeader").style.display = "none";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="viewSchedule();">View Amortization Schedule<\/button><p><i class="arrow up"></i></p>'

}

