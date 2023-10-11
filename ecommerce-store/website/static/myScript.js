if (window.location.href == "http://127.0.0.1:5000/checkout") {

window.setInterval(function(){
    emailValue = document.getElementById("emailtxt").value;
    cardValue = document.getElementById("cardtxt").value;
    expiryValue = document.getElementById("expirytxt").value;
    cvvValue = document.getElementById("cvvtxt").value;
    firstnameValue = document.getElementById("firstnametxt").value;
    secondnameValue = document.getElementById("secondnametxt").value;

    var emailRE = /\S+@\S+\.\S+/;
    var expiryRE = /\d\d\s\/\s\d\d/i;
    
    // --------------------------------------------------------------------------------
    if (emailRE.test(emailValue) && emailValue.length > 0) {
        document.getElementById("email").innerHTML = "";
        document.getElementById("emailtxt").style.border = "2px solid green";
        document.getElementById("emaillbl").style.color = "green";
    } 
    else if (!(emailRE.test(emailValue)) && emailValue.length != 0) {
        document.getElementById("email").innerHTML = "Email must match : example@example.com";
        document.getElementById("emailtxt").style.border = "2px solid red";
        document.getElementById("emaillbl").style.color = "red";                        
    }
    else {
        document.getElementById("email").innerHTML = "";
        document.getElementById("emailtxt").style.border = "";
        document.getElementById("emaillbl").style.color = "";                        
    }
    // --------------------------------------------------------------------------------
    
    // --------------------------------------------------------------------------------
    if (cardValue.length == 19) {
        document.getElementById("card").innerHTML = "";
        document.getElementById("cardtxt").style.border = "2px solid green";
        document.getElementById("cardlbl").style.color = "green";
    } 
    else if (cardValue.length < 19 && cardValue.length != 0) {
        document.getElementById("card").innerHTML = "Credit card number must be 16 digits.";
        document.getElementById("cardtxt").style.border = "2px solid red";
        document.getElementById("cardlbl").style.color = "red";
    }
    else {
        document.getElementById("card").innerHTML = "";
        document.getElementById("cardtxt").style.border = "";
        document.getElementById("cardlbl").style.color = "";
    }
    // --------------------------------------------------------------------------------

    // --------------------------------------------------------------------------------
    if (expiryRE.test(expiryValue) && expiryValue.length == 7) {
            document.getElementById("expiry").innerHTML = "";
            document.getElementById("expirytxt").style.border = "2px solid green";
            document.getElementById("expirylbl").style.color = "green";
        }
        else if (!(expiryRE.test(expiryValue)) && expiryValue.length != 0) {
            document.getElementById("expiry").innerHTML = "Expiry must match : MM / YY.";
            document.getElementById("expirytxt").style.border = "2px solid red";
            document.getElementById("expirylbl").style.color = "red";
        }
        else {
            document.getElementById("expiry").innerHTML = "";
            document.getElementById("expirytxt").style.border = "";
            document.getElementById("expirylbl").style.color = "";
        }
    // --------------------------------------------------------------------------------

    // --------------------------------------------------------------------------------
    if (cvvValue.length == 3) {
            document.getElementById("cvv").innerHTML = "";
            document.getElementById("cvvtxt").style.border = "2px solid green";
            document.getElementById("cvvlbl").style.color = "green";
        }
        else if (cvvValue.length != 3 && cvvValue.length != 0) {
            document.getElementById("cvv").innerHTML = "Three digits on back of card.";
            document.getElementById("cvvtxt").style.border = "2px solid red";
            document.getElementById("cvvlbl").style.color = "red";
        }
        else {
            document.getElementById("cvv").innerHTML = "";
            document.getElementById("cvvtxt").style.border = "";
            document.getElementById("cvvlbl").style.color = "";
        }
    // --------------------------------------------------------------------------------    

    // --------------------------------------------------------------------------------
    if (firstnameValue.length > 0) {
        document.getElementById("firstnametxt").style.border = "2px solid green";
        document.getElementById("firstnamelbl").style.color = "green";
    }
    else {
        document.getElementById("firstnametxt").style.border = "";
        document.getElementById("firstnamelbl").style.color = "";
    }
    // --------------------------------------------------------------------------------

    // --------------------------------------------------------------------------------
    if (secondnameValue.length > 0) {
        document.getElementById("secondnametxt").style.border = "2px solid green";
        document.getElementById("secondnamelbl").style.color = "green";
    }
    else {
        document.getElementById("secondnametxt").style.border = "";
        document.getElementById("secondnamelbl").style.color = "";
    }
    // --------------------------------------------------------------------------------
}, 500);


// Check validity of inputs
window.setInterval(function(){
    emailValue = document.getElementById("emailtxt").value;
    cardValue = document.getElementById("cardtxt").value;
    expiryValue = document.getElementById("expirytxt").value;
    cvvValue = document.getElementById("cvvtxt").value;
    firstnameValue = document.getElementById("firstnametxt").value;
    secondnameValue = document.getElementById("secondnametxt").value;

    var emailRE = /\S+@\S+\.\S+/;
    var expiryRE = /\d\d\s\/\s\d\d/i;

    if (
        (emailRE.test(emailValue) && emailValue.length > 0) && // Email test
        (cardValue.length == 19) && // Card test
        (expiryRE.test(expiryValue) && expiryValue.length == 7) && // Expiry test
        (cvvValue.length == 3) && // CVV test
        (firstnameValue.length > 0) && // First name test
        (secondnameValue.length > 0) // Second name test
    ) {
        document.getElementById("purchase").disabled = false;
        document.getElementById("checkout-card").style.boxShadow = "0 10px 20px green";
        document.getElementById("purchase").style.backgroundColor = "green";
        document.getElementById("purchase").style.border = "green";
    }  
    else {
        document.querySelector("#purchase").disabled = true;
        document.getElementById("checkout-card").style.boxShadow = "";
        document.getElementById("purchase").style.backgroundColor = "red";
        document.getElementById("purchase").style.border = "red";
        document.getElementById("purchase").style.color = "white";
    }
}, 500);

}

jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});
