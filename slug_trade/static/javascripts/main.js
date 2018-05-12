var editProfileFormTouched = function(first_name, last_name, bio, on_off_campus, profile_picture) {
  return (
    ($('#id_first_name').val() != first_name) ||
    ($('#id_last_name').val() != last_name) ||
    ($('#id_bio').val() != bio) ||
    ($('#id_on_off_campus').val() != on_off_campus) ||
    ($('#id_profile_picture').val() != profile_picture)
  )
};

var countHiddenPhotos = function() {
  var num_photos = 5;
  var id = '#picture';
  var count = 0;
  for(var i=1; i<=num_photos; i++) {
    var current_id = id+i;
    if($(current_id).css('display') == 'none') {
      count++;
    }
  }
  return count;
};

var canAddPhoto = function() {
  var num_photos = 5;
  var id = '#picture';
  console.log('here');
  for(var i=num_photos; i>=1; i--) {
    var current_id = id+i;
    if($(current_id).css('display') == 'block') {
      console.log($('#image'+i).val());
      return $('#image'+i).val() != '';
    }
  }
}

var showAddPhotoButton = function() {
  console.log(canAddPhoto());
  if(countHiddenPhotos() > 0) {
    $('#add_picture').css('display', 'block');
  }
};

var add_closet_item_image = 'https://image.freepik.com/free-icon/question-mark-in-a-circle-outline_318-53407.jpg';

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
    $(window).load(function () {
      $('#id_username').focus();
    });
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
  $(function() {
    $('#id_image1').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#add_closet_img1').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  $(function() {
    $('#id_image2').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#add_closet_img2').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  $(function() {
    $('#id_image3').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#add_closet_img3').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  $(function() {
    $('#id_image4').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#add_closet_img4').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  $(function() {
    $('#id_image5').change(function() {
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if(input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#add_closet_img5').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
      }
    });
  });

  $(function() {
    $('#close_img1').click(function() {
      $('#add_closet_img1').attr('src', add_closet_item_image);
      $('#id_image1').val('');
      if(countHiddenPhotos() < 4) {
        $('#picture1').css('display', 'none');
        showAddPhotoButton();
      }
    });
  });

  $(function() {
    $('#close_img2').click(function() {
      $('#add_closet_img2').attr('src', add_closet_item_image);
      $('#id_image2').val('');
      $('#picture2').css('display', 'none');
      showAddPhotoButton();
    });
  });

  $(function() {
    $('#close_img3').click(function() {
      $('#add_closet_img3').attr('src', add_closet_item_image);
      $('#id_image3').val('');
      $('#picture3').css('display', 'none');
      showAddPhotoButton();
    });
  });

  $(function() {
    $('#close_img4').click(function() {
      $('#add_closet_img4').attr('src', add_closet_item_image);
      $('#id_image4').val('');
      $('#picture4').css('display', 'none');
      showAddPhotoButton();
    });
  });

  $(function() {
    $('#close_img5').click(function() {
      $('#add_closet_img5').attr('src', add_closet_item_image);
      $('#id_image5').val('');
      $('#picture5').css('display', 'none');
      showAddPhotoButton();
    });
  });

  $(function() {
    $('#add_photo_img').click(function() {
      var id = '#picture';
      var num_photos = 5;
      for(var i=1; i<=num_photos; i++) {
        var current_id = id+i;
        if($(current_id).css('display') == 'none') {
          $(current_id).css('display', 'block');
          break;
        }
      }
      if(countHiddenPhotos() == 0) {
        $('#add_picture').css('display', 'none');
      }
    });
  });

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
