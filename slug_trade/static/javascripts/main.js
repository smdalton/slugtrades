var editProfileFormTouched = function(first_name, last_name, bio, on_off_campus, profile_picture) {
  return (
    ($('#id_first_name').val() != first_name) ||
    ($('#id_last_name').val() != last_name) ||
    ($('#id_bio').val() != bio) ||
    ($('#id_on_off_campus').val() != on_off_campus) ||
    ($('#id_profile_picture').val() != profile_picture)
  )
}

$(document).ready(function() {
  // show drop links on hover
  $(".links-drop, .links-box-wrapper").hover(function(){
      $('.links-box-wrapper').css('display','flex');
  },function(){
      $('.links-box-wrapper').css('display','none');
  });

  //inject placeholder text into login forms
  //on login page make login wrapper height of viewpoint
  if (location.pathname.substring(1) == "login/") {
    $('#id_username').attr('placeholder', 'Email Address');
    $('#id_password').attr('placeholder', 'Password');
    var height = $(window).height() - 86;
    $('.login-wrapper').css('height',height)
  }

  if (location.pathname.substring(1) == "edit_profile/") {
    let first_name = $('#id_first_name').val();
    let last_name = $('#id_last_name').val();
    let bio = $('#id_bio').val();
    let on_off_campus = $('#id_on_off_campus').val();
    let profile_picture = $('#id_profile_picture').val();
    $(window).on("beforeunload", function() {
      if(editProfileFormTouched(first_name, last_name, bio, on_off_campus, profile_picture)) {
        return 'Are you sure you want to leave?'; // custom alert messages are no longer supported in most browsers :(
      }
    });
    //turn off the beforeunload event upon form submission
    $(document).ready(function() {
      $("#edit_profile_form").on("submit", function(e) {
        $(window).off("beforeunload");
        return true;
      });
    });
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

  $(document).on('change', '#id_trade_options', function(e) {

    var dropChoice = this.options[e.target.selectedIndex].text;

    if(dropChoice == 'Cash Only') {
      $('.add-item-price').css('display','flex');
      $('#add-item-left').css('margin-right','10px');
    } else {
      $('.add-item-price').css('display','none');
      $('#add-item-left').css('margin-right','0');
    }



});

  // ---- These are functions that handle the hiding/showing of images
    // get it to show the next one
 $(function(){
   $('#show_2').click(function(e){
       e.preventDefault();
     $('#picture_2').css('display','flex');
       $('#show_2').hide()
   })
 })

 $(function(){
   $('#show_3').click(function(e){
       e.preventDefault();
     $('#picture_3').css('display','flex');
     $('#show_3').hide()
   })
 })

 $(function(){
   $('#show_4').click(function(e){
       e.preventDefault();
     $('#picture_4').css('display','flex');
     $('#show_4').hide()
   })
 })

 $(function(){
   $('#show_5').click(function(e){
       e.preventDefault();
     $('#picture_5').css('display','flex');
     $('#show_5').hide()
   })
 })




  // ---- all of these functions clear images out of the file selectors inside add_closet_item ----
  $(function() {
    $('#clear_image1').click(function() {
      $("#id_image1").val("");

    });
  });

  $(function() {
    $('#clear_image2').click(function() {
      $("#id_image2").val("");
      $("#picture_2").hide();
      $('#show_2').show();
    });
  });

  $(function() {
    $('#clear_image3').click(function() {
      $("#id_image3").val("");
      $("#picture_3").hide();
      $('#show_3').show();
    });
  });

  $(function() {
    $('#clear_image4').click(function() {
      $("#id_image4").val("");
      $("#picture_4").hide();
      $('#show_4').show();
    });
  });

  $(function() {
    $('#clear_image5').click(function() {
      $("#id_image5").val("");
      $("#picture_5").hide();
      //This needs to show the plus sign above it which is plus sign for show_5
      $('#show_5').show()
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

//Smooth scrolling on steps
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
