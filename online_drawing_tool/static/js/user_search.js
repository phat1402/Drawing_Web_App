/**
 * Created by user on 12/17/2016.
 */
$(function(){

// using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $('#user-search').on('keyup', function () {
        //if($('#search').val().length!==0)

        $.ajax({
           type: 'GET',
           url : 'api/user_search',
           data: {
               'user_search_text' : $('#user-search').val(),

           },
           success: function(response){

               $('#user_search_results').html(response)

           }
       })
    //}

    });

});