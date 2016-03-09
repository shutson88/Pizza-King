$(function() {

    $('#showLoginDialog').on('click', function(){
        $.loadmodal({
            url: '/homepage/login.loginForm',
            title: 'Login',
            width: '438px'
        });//modal
    });//click

    $('#searchBar').on('change', function (){
        var term = $(this).val();

        $(location).attr('href','/homepage/product.search/' + term);
    });//change

    $(".datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "2015:2100"
    });

});//ready