$(document).ready(function() {
    var data = "";
    data += "USER=seller_1333326312_biz_api1.taylorsavage.com";
    data += "&PWD=1333326337";
    data += "&SIGNATURE=AkIa1P7AJMEI4d4cuC7EVi15wBoHAKhoItg1rRg1bRSHugBdUTgeg7WY";
    data += "&VERSION=72.0";
    data += "&PAYMENTREQUEST_0_PAYMENTACTION=Sale";
    data += "&PAYMENTREQUEST_0_AMT=" + $("#deal_price").val();
    data += "&PAYMENTREQUEST_0_CURRENCYCODE=USD";
    data += "&L_PAYMENTREQUEST_0_NAME0=" + $("#deal_name").val();
    data += "&L_PAYMENTREQUEST_0_NUMBER0=" + $("#deal_pk").val();
    data += "&L_PAYMENTREQUEST_0_DESC0=" + $("#deal_description").val();
    data += "&L_PAYMENTREQUEST_0_AMT0=" + $("#deal_price").val();
    data += "&RETURNURL=https://glados.stanford.edu:8080/purchased/";
    data += "&CANCELURL=https://glados.stanford.edu:8080/";
    data += "&METHOD=SetExpressCheckout";
    $('#buy_button').click(function() {
        $.ajax({
            type: 'POST',
            url: 'https://api-3t.sandbox.paypal.com/nvp',
            data: data,
            success: reviewSetExpressCheckout,
        });
    });
});

function reviewSetExpressCheckout(data) {
    alert(data);
}