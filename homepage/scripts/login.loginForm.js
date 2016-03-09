$(function() {

    $('#loginForm').ajaxForm(function(data) {
        $('#jquery-loadmodal-js-body').html(data);
    });//ajaxForm

});//ready