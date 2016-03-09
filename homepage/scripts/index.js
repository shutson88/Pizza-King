$(function() {

    $('li.noParent').each(function() {
      var parentId = $( this ).attr('parent');
      if($('li#' + parentId).has('ul').length)
      {
          $('li#' + parentId + " > ul").append($(this));
      } else {
          $('li#' + parentId).append('<ul class="subCat hide"></ul>');
          $('li#' + parentId + " > ul").append($(this));
      }
    });

    $('#categoriesUl > li').on('click', function(event) {
        var top = $(this);
        top.addClass("active");
        $('#categoriesUl').find('ul').addClass('hide');
        $('#categoriesUl .active  ul').removeClass('hide');
        top.removeClass('active');
    });


    //$('#loginDialog').modal({
    //    show: false,
    //});//load modal

    //$('#showLoginDialog').on('click', function(){
    //    $('#loginDialog').modal('show');
    //    $.ajax({
    //        url: '/homepage/index.loginForm',
    ////
    ////        data: {
    ////            u: username
    ////        },//data
    ////
    ////        type: "POST",
    ////
    //        success: function(resp){
    //            $('#loginDialog').find('.modal-body').html(resp);
    //        },//success
    //    });//ajax
    //});//click

    //$('#loginForm').ajaxForm(function(data) {
    //    $('#loginFormContainer').html(data);
    //    console.log(data );
    //});//ajaxForm

    //$('#id_username').on('change', function(){
    //    var username = $(this).val();
    //    $.ajax({
    //        url: '/homepage/index.check_username/',
    //
    //        data: {
    //            u: username
    //        },//data
    //
    //        type: "POST",
    //
    //        success: function(resp){
    //            if(resp == '1'){
    //                $('#idUsernameMessage').text('Username checks out!');
    //            }
    //            else{
    //
    //            }//if
    //            console.log(resp);
    //        },//success
    //    });//ajax
    //});//change

});//ready