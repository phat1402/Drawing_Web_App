$('#login-button').click(function(){
  $('#login-button').fadeOut("slow",function(){
    $("#container").fadeIn();
    TweenMax.from("#container", .4, { scale: 0, ease:Sine.easeInOut});
    TweenMax.to("#container", .4, { scale: 1, ease:Sine.easeInOut});
    
    $("#container2").fadeIn();
    TweenMax.from("#container2", .4, { scale: 0, ease:Sine.easeInOut});
    TweenMax.to("#container2", .4, { scale: 1, ease:Sine.easeInOut});
  });
});

$(".close-btn").click(function() {
  
  TweenMax.from("#container", .4, {scale: 1, ease: Sine.easeInOut});
  TweenMax.to("#container", .4, {left: "0px", scale: 0, ease: Sine.easeInOut});
  $("#container, #registerc").fadeOut(800, function () {
    $("#login-button").fadeIn(800);
  });
  
  TweenMax.from("#container2", .4, {scale: 1, ease: Sine.easeInOut});
  TweenMax.to("#container2", .4, {left: "0px", scale: 0, ease: Sine.easeInOut});
  $("#container2, #registerc").fadeOut(800, function () {
    $("#login-button").fadeIn(800);
  });
  
});

/* Forgotten Password */
$('#forgotten').click(function(){
  
  $("#container").fadeOut(function(){
    $("#registerc").fadeIn();
  });
  
  $("#container2").fadeOut(function(){
    $("#registerc").fadeIn();
  });
  
});
