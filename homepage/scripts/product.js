$(function() {

    $('.cartAdd').on('click', function(){

        var pid = $(this).attr('data-pid');
        var qty = 1;

        $.loadmodal({
            url: "/homepage/cart.add/" + pid + "/" + qty,
            title: "Shopping Cart",
            width: '700px'
        });//loadModal
    });//click

});//ready