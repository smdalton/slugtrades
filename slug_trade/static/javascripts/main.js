var editProfileFormTouched = function(first_name, last_name, bio, on_off_campus, profile_picture) {
  return (
    ($('#id_first_name').val() != first_name) ||
    ($('#id_last_name').val() != last_name) ||
    ($('#id_bio').val() != bio) ||
    ($('#id_on_off_campus').val() != on_off_campus) ||
    ($('#id_profile_picture').val() != profile_picture)
  )
};

var clickItem = function(id) {
  window.location.href = '/edit_closet_item/?id='+id;
};

// add closet items helper functions and variables

var add_closet_item_image = 'https://image.freepik.com/free-icon/question-mark-in-a-circle-outline_318-53407.jpg';
var closet_photos = undefined;
var closet_files = undefined;
var closet_temps = undefined;

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

var countSelectedPhotos = function() {
  var num_photos = 5;
  var id = '#temp-image';
  var count = 0;
  for(var i=1; i<=num_photos; i++) {
    var current_id = id+i;
    if($(current_id).val() != '') {
      count++;
    }
  }
  return count;
};

var canAddPhoto = function() {
  if(countHiddenPhotos() == 5) {
    return true;
  }
  for(var i=closet_photos.length-1; i>=0; i--) {
    var current_id = closet_photos[i];
    if($('#' + current_id).css('display') == 'block') {
      var image = $('#' + closet_temps[i]).val();
      return image != '';
    }
  }
}

var showAddPhotoButton = function() {
  if(countHiddenPhotos() > 0) {
    $('#add_picture').css('display', 'block');
  }
};

var swapArrayElements = function(arr, index1, index2) {
  var temp = arr[index1];
  arr[index1] = arr[index2];
  arr[index2] = temp;
}

var swapDivElements = function(id1, id2) {
  obj1 = document.getElementById(id1);
  obj2 = document.getElementById(id2);
  // create marker element and insert it where obj1 is
  var temp = document.createElement("div");
  obj1.parentNode.insertBefore(temp, obj1);

  // move obj1 to right before obj2
  obj2.parentNode.insertBefore(obj1, obj2);

  // move obj2 to right before where obj1 used to be
  temp.parentNode.insertBefore(obj2, temp);

  // remove temporary marker node
  temp.parentNode.removeChild(temp);

  var index1 = closet_photos.indexOf(id1);
  var index2 = closet_photos.indexOf(id2)
  swapArrayElements(closet_photos, index1, index2);
  swapArrayElements(closet_files, index1, index2);
  swapArrayElements(closet_temps, index1, index2);
}

// function moves any unselected photos to the back of the container, so that
// the user is always entering photos at the back of the list
var shuffle = function() {
  for(var i=0; i<closet_files.length-1; i++) {
    curr_id = closet_temps[i];
    next_id = closet_temps[i+1];
    if($('#'+curr_id).val() == '' && $('#'+next_id).val() != '') {
      var photo1 = closet_photos[closet_temps.indexOf(curr_id)];
      var photo2 = closet_photos[closet_temps.indexOf(next_id)];
      swapDivElements(photo1, photo2);
    }
  }
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

  // --- ADD CLOSET ITEM EVENTS --------------------------------------------------------------------------

  // ---- These functions show photo previews in add closet itm
  closet_photos = ['picture1', 'picture2', 'picture3', 'picture4', 'picture5'];
  closet_files = ['id_image1', 'id_image2', 'id_image3', 'id_image4', 'id_image5'];
  closet_temps = ['temp-image1', 'temp-image2', 'temp-image3', 'temp-image4', 'temp-image5']

  $(function() {
    $('#id_image1').change(function() {
      var input = this;
      var url = $(this).val();
      $('#temp-image1').val(url);
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
      $('#temp-image2').val(url);
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
      $('#temp-image3').val(url);
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
      $('#temp-image4').val(url);
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
      $('#temp-image5').val(url);
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

  //---- These functions handle the logic when you click an x on the photos

  $(function() {
    $('#close_img1').click(function() {
      $('#add_closet_img1').attr('src', add_closet_item_image);
      $('#id_image1').val('');
      $('#temp-image1').val('');
      $('#picture1').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img2').click(function() {
      $('#add_closet_img2').attr('src', add_closet_item_image);
      $('#id_image2').val('');
      $('#temp-image2').val('');
      $('#picture2').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img3').click(function() {
      $('#add_closet_img3').attr('src', add_closet_item_image);
      $('#id_image3').val('');
      $('#temp-image3').val('');
      $('#picture3').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img4').click(function() {
      $('#add_closet_img4').attr('src', add_closet_item_image);
      $('#id_image4').val('');
      $('#temp-image4').val('');
      $('#picture4').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img5').click(function() {
      $('#add_closet_img5').attr('src', add_closet_item_image);
      $('#id_image5').val('');
      $('#temp-image5').val('');
      $('#picture5').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  // ---- This function handles the logic when you click add photo

  $(function() {
    $('#add_picture').click(function() {
      if(canAddPhoto()) {
        shuffle();
        for(var i=0; i<closet_photos.length; i++) {
          var current_id = '#'+closet_photos[i];
          if($(current_id).css('display') == 'none') {
            $(current_id).css('display', 'block');
            $('#'+closet_files[i]).trigger('click');
            break;
          }
        }
        if(countHiddenPhotos() == 0) {
          $('#add_picture').css('display', 'none');
        }
      } else {
        alert('You must choose a photo first.');
      }
    });
  });

  // -- Validation for add closet item form
  $(function() {
    $('#add-closet-submit').click(function(event) {
      if($('#id_name').val() != '' && $('#id_description').val() != '' && countSelectedPhotos() == 0) {
        alert('You must add a photo!');
        event.preventDefault();
      }
    });
  });

// ------------------ END OF ADD ADD CLOSET ITEM FUNCTIONS --------------------
  //this function deletes an item from the wishlist on the profile

  // ---------------- WISHLIST FUNCTIONS ------------------------------------
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

// --------------- END OF WISHLIST FUNCTIONS ------------------------

//Smooth scrolling on steps
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
