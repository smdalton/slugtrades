$(document).ready(function() {

  console.log("Javascript is working!");

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
  //this function deletes an item from the wishlist on the profile
  $(function() {
    $('.delete_from_wishlist').click(function() {
      let id = $(this).val();
      $.ajax({
        type: "POST",
        url: "/delete_from_wishlist/",
        data: {id: id}
      });
      $('#wishlist_' + String(id)).css('display', 'none');
    });
  });

  //auto scroll to wishlist if an item was just added
  if($('#wishlist_scroll_anchor').offset() != undefined) {
    $('html, body').animate({
          scrollTop: $('#wishlist_scroll_anchor').offset().top
      }, 1);
    $('#wishlist_item_description').focus();
  }
});
