/**
 * Created by root on 13/1/18.
 */
$(document).ready(function () {
    $('#iban').mask('DE00 0000 0000 0000 0000 00', {
        placeholder: '____ ____ ____ ____ ____ __'
    });
});
$("#iban").change(function () {
    str = document.getElementById('iban').value;
    document.getElementById("bic").disabled = true;
    document.getElementById("bankName").disabled = true;
    console.log(str);
    str = str.replace(/ /g, "");
    // str=str.replace(" ","");
    console.log(str);
    // body...
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
        document.getElementById("bankName").disabled = false;
        document.getElementById("bankName").value = data.bankData.name;
        console.log(data.bankData.name);
    });
});
