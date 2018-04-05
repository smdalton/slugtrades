
$(document).ready(function() {

  alert("Javascript is working!");

  //toggles image on products page
  var isVisible = false;
  $("#toggle-button").click(function(){
      if (!isVisible) {
        $(".pop-img").css("display", "block");
        isVisible = true;
      } else {
        $(".pop-img").css("display", "none");
        isVisible = false;
      }
  });
});
