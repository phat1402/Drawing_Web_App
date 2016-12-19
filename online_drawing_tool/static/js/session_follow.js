/**
 * Created by user on 12/17/2016.
 */
$(document).ready(function() {
    var loaded =false;
    if(loaded) return;

        getfollower();
        getfollowing();
    loaded =true;
}) ;

var getfollower= (function(){
    //var u = document.getElementById('EditModeId').value;
    $.ajax({
           type: 'GET',
           url : 'api/sessfollower',
       //    data: {
       //        'u' : u.toString()
       //    },
           success: function(response){

               $('#follower-count').html(response)

           }
       })

});

var getfollowing=(function(){
    //var u = document.getElementById('EditModeId').value;
    $.ajax({
           type: 'GET',
           url : 'api/sessfollowing',
        //   data: {
        //       'u' : u.toString()
         //  },
           success: function(response){

               $('#following-count').html(response)

           }
       })

});