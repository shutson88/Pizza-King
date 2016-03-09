$(function() {

    totalDue = 0.00;
    $('.rentalPrice').each(function(){
        var pQty = $(this).next().children().val();
        totalDue += (parseFloat($(this).text()) * pQty);
    });//each
    $('#id_amount').val(totalDue.toFixed(2));

    $('#couponImg').on('click', function (){
        var newTotal = totalDue * .8;
        $('#id_amount').val(newTotal.toFixed(2));
    });//click

    $('#submitOrder').on('click', function (){
        $('#id_amount').removeAttr("disabled");
        $(location).attr('href','/homepage/checkout.thanks');
    });//click

    $('.productDelete').on('click', function (){
        var productId = $(this).attr('data-pid');
        $.get('/homepage/checkout.delete/' + productId);//ajax
        $(this).parent().parent().remove();
    });//click

    $('.productUpdate').on('click', function (){
        var productId = $(this).attr('data-pid');
        var pQty = $(this).parent().prev().children().val();
        $.get('/homepage/checkout.update/' + productId + "/" + pQty);//ajax
        $(".alert").show().delay(2000).fadeOut();

    });//click

    $('#cartContainer').on('change', function(){
        totalDue = 0.00;
        $('.rentalPrice').each(function(){
            var pQty = $(this).next().children().val();
            totalDue += (parseFloat($(this).text()) * pQty);
        });//each
        $('#id_amount').val(totalDue.toFixed(2));

    });//change

});//ready