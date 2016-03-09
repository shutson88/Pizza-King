$(function() {

    $('.cartDelete').on('click', function (){
        var pId = $(this).attr('data-pid');
        $.get("/homepage/cart.delete/" + pId);//ajax
        $(this).parent().parent().remove();
    });//click

    $('.cartUpdate').on('click', function (){
        var pId = $(this).attr('data-pid');
        var pQty = $(this).parent().prev().children().val();
        $.get("/homepage/cart.update/" + pId + "/" + pQty);//ajax

        $(".alert").show().delay(800).fadeOut();

    });//click

    $('#checkout').on('click', function (){
        $(location).attr('href','/homepage/checkout');
    });//click

});//ready