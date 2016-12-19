/**
 * Created by user on 12/17/2016.
 */
/**
 * Created by user on 12/9/2016.
 */
function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
$(document).ready(function() {
    var loaded =false;
    var u = {{username}};
    if(loaded) return;
       $.ajax({
           type: 'GET',
           url : 'api/follow',
           data: {
               'u' : u.toString()
           },
           success: function(response){

               $('#result').html(response)

           }
       })
        getfollower();
        getfollowing();
    loaded =true;
}) ;

var getfollower= (function(){
    var u = {{username}};
    $.ajax({
           type: 'GET',
           url : 'api/getfollower',
           data: {
               'u' : u.toString()
           },
           success: function(response){

               $('#follower-count').html(response)

           }
       })

});

var getfollowing=(function(){
    var u = {{username}};
    $.ajax({
           type: 'GET',
           url : 'api/getfollowing',
           data: {
               'u' : u.toString()
           },
           success: function(response){

               $('#following-count').html(response)

           }
       })

});