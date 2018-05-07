$(document).ready(function() {

  // show drop links on hover
  $(".links-drop, .links-box-wrapper").hover(function(){
      $('.links-box-wrapper').css('display','flex');
  },function(){
      $('.links-box-wrapper').css('display','none');
  });

  //inject placeholder text into login forms
  if (location.pathname.substring(1) == "login/") {
    $('#id_username').attr('placeholder', 'Email Address');
    $('#id_password').attr('placeholder', 'Password');
  }

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

  // ---- These are functions that handle the hiding/showing of images
    // get it to show the next one
 $(function(){
   $('#show_2').click(function(e){
       e.preventDefault();
     $('#picture_2').show()
       $('#show_2').hide()
   })
 })

 $(function(){
   $('#show_3').click(function(e){
       e.preventDefault();
     $('#picture_3').show()
     $('#show_3').hide()
   })
 })

 $(function(){
   $('#show_4').click(function(e){
       e.preventDefault();
     $('#picture_4').show()
     $('#show_4').hide()
   })
 })

 $(function(){
   $('#show_5').click(function(e){
       e.preventDefault();
     $('#picture_5').show()
     $('#show_4').hide()
   })
 })




  // ---- all of these functions clear images out of the file selectors inside add_closet_item ----
  $(function() {
    $('#clear_image1').click(function() {
      $("#id_image1").val("");
    });
  });

  $(function() {
    $('#clear_image1').click(function() {
      $("#id_image2").val("");
      $("#id_image2").val("");
      $("#id_image2").hide();
      $('#show_2').show();
    });
  });

  $(function() {
    $('#clear_image3').click(function() {
      $("#id_image3").val("");
      $("#id_image3").hide();
      $('#show_3').show();
    });
  });

  $(function() {
    $('#clear_image4').click(function() {
      $("#id_image4").val("");
      $("#id_image4").hide();
      $('#show_4').show();
    });
  });

  $(function() {
    $('#clear_image5').click(function() {
      $("#id_image5").val("");
      $("#id_image5").hide();
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
