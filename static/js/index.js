$(document).ready(function() {
    $("#btnCalculate").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val().replace(/[*,]/g, ""),
            interestRate: $("#txtInterestRate").val().replace(/[*,]/g, ""),
            yearsToRepay: $("#txtYearsToRepay").val().replace(/[*,]/g, "")
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result.toFixed(2));
            $("#scheduleTable").html('<h2 id="scheduleHeader">Amortization Schedule<h2>' + data.schedule);
            $("#txtExtraPayment").val("");
            $("#payDetails").html("");
            hideSchedule();
        });
        return false;
    });
});

$(document).ready(function() {
    $("#btnApplyExtraPay").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_explore_payment", {
            loanAmount: $("#txtLoanAmount").val().replace(/[*,]/g, ""),
            interestRate: $("#txtInterestRate").val().replace(/[*,]/g, ""),
            yearsToRepay: $("#txtYearsToRepay").val().replace(/[*,]/g, ""),
            extraPayment: $("#txtExtraPayment").val().replace(/[*,]/g, "")
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result.toFixed(2));
            $("#scheduleTable").html('<h2 id="scheduleHeader">Amortization Schedule<h2>' + data.schedule);
            $("#payDetails").html('<p class="overview exploreOverview">Your monthly payment is $' + data.originalPayment + 
                ". By paying extra, " + data.details + '</p>');
            hideSchedule();
        });
        return false;
    });
});

$(document).ready(function() { 
    $("#exploreTop").click(function() {
        let displayVal = $("#exploreHidden").css("display");
        if (displayVal == "none") {
            $("#viewExplore").html("Hide Explore");
            $("#exploreArrow").html('<i class="arrow down"></i>');
            $("#exploreHidden").css("display", "block");
        } else {
            $("#viewExplore").html("View Explore");
            $("#exploreArrow").html('<i class="arrow up"></i>');
            $("#exploreHidden").css("display", "none");
        }
    });
});

$('input.number').keyup(function(event) {

    // skip for arrow keys
    if(event.which >= 37 && event.which <= 40) return;

    // format input numbers
    $(this).val(function(index, value) {
        let inputId = $(this).attr("id");
        if (inputId == "txtYearsToRepay" && value.length > 2) {
            return value.slice(0, 2);
        }

        for (let i = 0; i < value.length; i++) {
            if (value[i] == ".") {
                let remainder = value.slice(i + 1);
                if (remainder.length > 2) {
                    return value.slice(0, i + 3);
                }
            }
        }
        return value.replace(/[*,]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    });
  })

function viewSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "table"; // data.schedule (returned from server) ID selector is scheduleDataFrame
    document.getElementById("scheduleHeader").style.display = "block";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="hideSchedule();">Hide Amortization Schedule<\/button><p><i class="arrow down"></i></p>';
}

function hideSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "none"; 
    document.getElementById("scheduleHeader").style.display = "none";
    document.getElementById("scheduleViewButton").innerHTML = '<button id="btnSchedule" onclick="viewSchedule();">View Amortization Schedule<\/button><p><i class="arrow up"></i></p>';
}