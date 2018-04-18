
$(document).ready(function() {
  console.log("Javascript is working!");
  //toggles image on products page
  var isVisible = false;
  $("#toggle-button").click(function(){
    if(!isVisible) {
      $(".pop-img").css("display", "block");
      isVisible = true;
    } else {
      $(".pop-img").css("display", "none");
      isVisible = false;
    }
  });

  $(function() {
    $('#upload').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#img').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });
});
