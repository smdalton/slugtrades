$(document).ready(function() {

  // show drop links on hover
  $(".links-drop, .links-box-wrapper").hover(function(){
      $('.links-box-wrapper').css('display','flex');
  },function(){
      $('.links-box-wrapper').css('display','none');
  });


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

  //on login page make login wrapper height of viewpoint
  if (location.pathname.substring(1) == "login/") {
    var height = $(window).height() - 86;
    $('.login-wrapper').css('height',height)
  }

//displays a preview of profile picture in edit_profile page
  $(function() {
    $('#id_file').change(function() {
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

  //displays a preview of profile picture in signup page
  $(function() {
    $('#id_profile_picture').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#signup_img').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  // ---- all of these functions clear images out of the file selectors inside add_closet_item ----
  $(function() {
    $('#clear_image1').click(function() {
      console.log('here');
      $("#id_image1").val("");
    });
  });

  $(function() {
    $('#clear_image2').click(function() {
      $("#id_image2").val("");
    });
  });

  $(function() {
    $('#clear_image3').click(function() {
      $("#id_image3").val("");
    });
  });

  $(function() {
    $('#clear_image4').click(function() {
      $("#id_image4").val("");
    });
  });

  $(function() {
    $('#clear_image5').click(function() {
      $("#id_image5").val("");
    });
  });
  // -- endblock -----

});


//Smooth scrolling on steps
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
