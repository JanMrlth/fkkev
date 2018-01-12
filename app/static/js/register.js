/**
 * Created by root on 12/1/18.
 */

var flag = 1;
function show(str1, str2) {
    console.log(str1, str2);
    // body...
    var showDiv = document.getElementById(str2);
    var hideDiv = document.getElementById(str1);
    hideDiv.style.display = "none";
    showDiv.style.display = "block";
    if (flag == 1) {
        console.log(flag);
        document.getElementById("flag_one").style.display = "inline";
    }
    else {
        console.log(flag);
        document.getElementById("flag_two").style.display = "inline";
    }
    document.getElementById("bName").value = document.getElementById("fName").value + " " + document.getElementById("lName").value;

}
function showType(selector) {
    console.log(selector);
    if (selector == 1) {
        // body...
        alert("Membership Type: Ordentliches Mitglied");    //Ordinary Member
        document.getElementById("topVAl").value = 0; //Ordinary Member
        document.getElementById('firma').style.display = "none";
        flag = 1;
    }
    else {
        alert("Membership Type: Förder-mitglied");      //Sustaining Member
        document.getElementById('firma').style.display = "inline";
        document.getElementById("topVAl").value = 2;    //Natural Person
        flag = 0;
    }
}

function changePayment(num) {
    console.log(num);
    document.getElementById("payment").value = num;
}

function changePayment__two(num2) {
    document.getElementById("payment__two").value = num2;
}


$(document).ready(function () {
    $('#iban').mask('DE00 0000 0000 0000 0000 00', {
        placeholder: '____ ____ ____ ____ ____ __'
    });

    $("#cName").change(function () {
        val = document.getElementById('cName').value;
        console.log('In cname');
        if (val.length > 0) {
            document.getElementById("natPer").style.display = "none";
            document.getElementById("jurPer").style.display = "inline";
            alert("Changed to: Juristische Person");
            document.getElementById("topVAl").value = 1; //Legal
            document.getElementById("bDay_toggle").style.display = "none";
            console.log(val.length)
        }
        else {
            console.log(val);
            document.getElementById("jurPer").style.display = "none";
            document.getElementById("natPer").style.display = "inline";
            alert("Changed to: Natürliche Person");
            document.getElementById("topVAl").value = 2 ;  //Natural
            document.getElementById("bDay_toggle").style.display = "block";

        }
    });

    $("#iban").change(function () {
        str = document.getElementById('iban').value;
        document.getElementById("bic").disabled = true;
        $.ajax({
            type: "GET",    //GET or POST
            url: 'https://openiban.com/validate/' + str + '?getBIC=true',    // Location of the service
            dataType: "json",   //Expected data format from server
            processdata: true   //True or False
        }).done(function (data) {
            console.log(data);
            console.log(data.bankData.bic);
            // document.getElementById("bic").disabled = false;
            valBIC = data.bankData.bic;
            document.getElementById("bic").value = valBIC;
            document.getElementById("bic").disabled = false;
        }).error(function (err) {
            console.log("Error:-" + err);
            document.getElementById("bic").disabled = false;
        });
    });

    $("#plz").change(function () {
        document.getElementById("city").disabled = true;
        zip = document.getElementById("plz").value;
        $.ajax({
            type: "GET",    //GET or POST
            url: 'http://api.zippopotam.us/DE/' + zip,    // Location of the service
            dataType: "json",   //Expected data format from server
            processdata: true   //True or False
        }).done(function (data) {
            console.log(data.places[0]);
            places = data['places'][0];
            document.getElementById("city").disabled = false;
            document.getElementById("city").value = places['place name'];
            console.log("city is:");
        }).error(function (err) {
            if(err){
                document.getElementById("city").disabled = false;
                document.getElementById("city").placeholder = 'Not Found City';
            }
        });

    });
});
//
var valBIC = 0;
