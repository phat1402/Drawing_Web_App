/**
 * Created by USER on 12/5/2016.
 */
/*-- like button --*/

$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrf
token = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('button').on('click', function () {
        // change button type by clicking
        $('.heart-shaped').toggle();

        // initailize
        var rand = Math.floor((Math.random() * 100) + 1);
        var flows = ["flows"];
        var colors = ["heart-particle-col"];
        var timing = (1.3).toFixed(1);

        // Animate Particle
        $('<div class="heart-particle part-' + rand + ' ' + colors[Math.floor((Math.random()))] + '" style="font-size:' + Math.floor(Math.random() * (28 - 12)) + 'px;"><i class="fa fa-heart"></i><i class="fa fa-heart"></i></div>').appendTo('.heart-particle-box').css({
            animation: "" + flows[Math.floor((Math.random()))] + " " + timing + "s linear"
        });
        $('.part-' + rand).show();
        // Remove Particle
        setTimeout(function () {
            $('.part-' + rand).remove();
        }, timing * 1000 - 100);
    });
});


/* like counting */
$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // $('.post-likes').click(function () {
    //
    //     var id, num_likes, liked;
    //     id = $('.heart-particle-box').attr('data-post-id');
    //     num_likes = $('#heart-counter').attr('data-num-likes');
    //     liked = $('.heart-particle-box').attr('data-liked');
    //     $.ajax({
    //         type: 'GET',
    //         url : 'api/like_blog',
    //         data:{
    //             post_id:id,
    //             num_likes:num_likes,
    //             liked:liked
    //         },
    //         success: function(response){
    //             //$('.like_count_blog').html(response);
    //             location.reload();
    //         }
    //     })
    // });

    $('.post-likes').click(function () {

           var id, num_likes, liked;
           id = $('.heart-particle-box').attr('data-post-id');
           num_likes = $('#heart-counter').attr('data-num-likes');
           liked = $('.heart-particle-box').attr('data-liked');
           $.ajax({
               type: 'GET',
               url : 'api/like_blog',
               dataType: 'json',
               data:{
                   post_id:id,
                   num_likes:num_likes,
                   liked_db:liked
               },
               success: function(response){
                   //alert (response.liked);
                   $('.like_count_blog').html(response.likes);
                   $('.heart-particle-box').attr('data-liked',response.liked);
                   //location.reload();
               }
           })
       });
});