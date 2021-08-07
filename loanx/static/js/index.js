
/**
 * Parses the monthly payment calculator form. The form values are sent to the 
 * server, and the server returns the required monthly payment amount and an HTML 
 * formatted table containing the amortization schedule.
 * 
 * @return {boolean} false: keeps page from reloading after request to server
 */
$(document).ready(function() {
    $("#btnCalculate").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_monthly_payment", {
            loanAmount: $("#txtLoanAmount").val().replace(/[*,]/g, ""),
            interestRate: $("#txtInterestRate").val().replace(/[*,]/g, ""),
            yearsToRepay: $("#txtYearsToRepay").val().replace(/[*,]/g, "")
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result);
            $("#scheduleTable").html('<h2 id="scheduleHeader">Amortization Schedule<h2>' + data.schedule);
            $("#txtExtraPayment").val("");
            $("#payDetails").html("");
            hideSchedule();
        });
        return false;
    });
});


/**
 * Parses both the monthly payment calculator and Explore section forms. The Explore 
 * form allows the user to add an extra dollar amount to their monthly payments
 * to explore paying their loan off quicker. The form values are sent to the server, 
 * and the server returns the required monthly payment amount, increased monthly 
 * payment amount, an HTML formatted table of the amortization schedule, and details 
 * of the shorter repayment period.
 * 
 * @return {boolean} false: keeps page from reloading after request to server
 */
$(document).ready(function() {
    $("#btnApplyExtraPay").click(function() {
        $.getJSON($SCRIPT_ROOT + "/get_explore_payment", {
            loanAmount: $("#txtLoanAmount").val().replace(/[*,]/g, ""),
            interestRate: $("#txtInterestRate").val().replace(/[*,]/g, ""),
            yearsToRepay: $("#txtYearsToRepay").val().replace(/[*,]/g, ""),
            extraPayment: $("#txtExtraPayment").val().replace(/[*,]/g, "")
        }, function(data) {
            $("#monthlyPayment").html("$" + data.result);
            $("#scheduleTable").html('<h2 id="scheduleHeader">Amortization Schedule<h2>' + data.schedule);
            $("#payDetails").html('<p class="overview exploreOverview">Your monthly payment is $' + data.originalPayment + 
                ". By paying extra, " + data.details + '</p>');
            hideSchedule();
        });
        return false;
    });
});


/**
 * Handles showing and hiding the Explore section.
 */
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


/**
 * Limits key presses to numbers and other needed keys for the input fields.
 */
$(document).ready(function(){  
    $("input.number").keydown(function(event) {  
        let allowedKeyCodes = new Set();

        // allow key codes for both number row and number pad
        for (let i = 48; i < 58; i++) {
            allowedKeyCodes.add(i);
            allowedKeyCodes.add(i + 48);
        }
        
        // allow key codes for arrow keys
        for (let i = 37; i < 41; i++) {
            allowedKeyCodes.add(i);
        }

        // allow key codes for period, delete, and backspace keys
        allowedKeyCodes.add(8); 
        allowedKeyCodes.add(46); 
        allowedKeyCodes.add(190);

       // dis-allow all other keyboard codes
       if (!allowedKeyCodes.has(event.which)) {
           event.preventDefault();
        }
    });  
}); 


/**
 * Formats numbers for the input fields.
 */
$(document).ready(function() {
    $("input.number").keyup(function(event) {

        // skip for arrow keys
        if(event.which >= 37 && event.which <= 40) return;
    
        // format input field numbers
        $(this).val(function(index, value) {
            let inputId = $(this).attr("id");
            if (value[0] == '0') return "";
            if (inputId == "txtYearsToRepay" && value.length > 2) {
                return value.slice(0, 2);
            }
    
            for (let i = 0; i < value.length; i++) {
                let allowedASCII = new Set([46, 44]); // ASCII codes for comma and period
                let ascii = value[i].charCodeAt(0);
    
                // limit input field to numbers and allowed ASCII encodings
                if ((ascii < 48 || ascii > 57) && !allowedASCII.has(ascii)) {
                    return value.slice(0, i);
                }
            }
            return value.replace(/[*,]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        });
    })
});

/**
 * Attaches a delegated event handler to the schedule view/hide button.
 */
$(document).on("click", "#btnSchedule", function() {
    let displayVal = document.getElementById("scheduleDataFrame").style.display;
    if (displayVal == "none") {
        viewSchedule();
    } else {
        hideSchedule();
    }
});


/**
 * Shows the amortization schedule and changes the text of its related view button.
 * @function viewSchedule
 */
function viewSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "table"; // data.schedule (returned from server) ID selector is scheduleDataFrame
    document.getElementById("scheduleHeader").style.display = "block";
    document.getElementById("scheduleViewButton").innerHTML = '<button type="button" id="btnSchedule">Hide Amortization Schedule<\/button><p><i class="arrow down"></i></p>';
}


/**
 * Hides the amortization schedule and changes the text of its related view button.
 * @function hideSchedule
 */
function hideSchedule() {
    document.getElementById("scheduleDataFrame").style.display = "none"; 
    document.getElementById("scheduleHeader").style.display = "none";
    document.getElementById("scheduleViewButton").innerHTML = '<button type="button" id="btnSchedule">View Amortization Schedule<\/button><p><i class="arrow up"></i></p>';
}

/**
 * Limits input fields to two decimal places, excluding the input field with 
 * ID "textYearsToRepay". The excluded input field with ID "textYearsToRepay" 
 * is, instead, limited to positive whole numbers < 100.
 * @param {*} e 
 */
function validate(e) {
    let inputId = e.id;
    let t = e.value;
    if (inputId == "txtYearsToRepay") {
        e.value = t.substr(0, 2);
    } else if (t.includes(".")) {
        e.value = t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3);
    }
}