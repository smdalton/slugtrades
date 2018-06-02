var navRedirect = function(url) {
  window.location.href = url;
};

var scrollToElement = function(id) {
  $('html, body').animate({
    scrollTop: $('#'+id).offset().top
  }, 1000);
};

// This is the function that manipulates the url when pagination controlls are clicked
var changePage = function(pageNumber) {
  var url = window.location.href;
  if(url.search(/page=\d+/i) == -1) {
    if(url.search(/\?/i) == -1) {
      var newUrl = url + '?page='+ pageNumber;
    } else {
      var newUrl = url + '&page=' + pageNumber;
    }
    window.location.href = newUrl;
  } else {
    var newUrl = url.replace(/page=\d+/i, 'page='+pageNumber);
    window.location.href = newUrl
  }
};

var editProfileFormTouched = function(firstName, lastName, bio, onOffCampus, profilePicture) {
  return (
    ($('#id_first_name').val() != firstName) ||
    ($('#id_last_name').val() != lastName) ||
    ($('#id_bio').val() != bio) ||
    ($('#id_on_off_campus').val() != onOffCampus) ||
    ($('#id_profile_picture').val() != profilePicture)
  )
};


var editItemTouched = function(name, category, tradeOptions, price, description, condition, image1, image2, image3, image4, image5) {
  return (
    ($('#id_name').val() != name) ||
    ($('#id_category').val() != category) ||
    ($('#id_trade_options').val() != tradeOptions) ||
    ($('#id_price').val() != price) ||
    ($('#id_description').val() != description) ||
    ($('#id_condition').val() != condition) ||
    ($('#temp-image1').val() != image1) ||
    ($('#temp-image2').val() != image2) ||
    ($('#temp-image3').val() != image3) ||
    ($('#temp-image4').val() != image4) ||
    ($('#temp-image5').val() != image5)
  )
};

var clickItem = function(id) {
  window.location.href = '/edit_closet_item/?id='+id;
};

// add closet items helper functions and variables

var addClosetItemDefaultImage = 'https://image.freepik.com/free-icon/question-mark-in-a-circle-outline_318-53407.jpg';
var closetPhotos = undefined;
var closetFiles = undefined;
var closetTemps = undefined;

var countHiddenPhotos = function() {
  var num_photos = 5;
  var id = '#picture';
  var count = 0;
  for(var i=1; i<=num_photos; i++) {
    var currentId = id+i;
    if($(currentId).css('display') == 'none') {
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
    var currentId = id+i;
    if($(currentId).val() != '') {
      count++;
    }
  }
  return count;
};

var canAddPhoto = function() {
  if(countHiddenPhotos() == 5) {
    return true;
  }
  for(var i=closetPhotos.length-1; i>=0; i--) {
    var currentId = closetPhotos[i];
    if($('#' + currentId).css('display') == 'block') {
      var image = $('#' + closetTemps[i]).val();
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


  $('.pgwSlider').pgwSlider();


  var index1 = closetPhotos.indexOf(id1);
  var index2 = closetPhotos.indexOf(id2)
  swapArrayElements(closetPhotos, index1, index2);
  swapArrayElements(closetFiles, index1, index2);
  swapArrayElements(closetTemps, index1, index2);
}

// function moves any unselected photos to the back of the container, so that
// the user is always entering photos at the back of the list
var shuffle = function() {
  for(var i=0; i<closetFiles.length-1; i++) {
    currId = closetTemps[i];
    nextId = closetTemps[i+1];
    if($('#'+currId).val() == '' && $('#'+nextId).val() != '') {
      var photo1 = closetPhotos[closetTemps.indexOf(currId)];
      var photo2 = closetPhotos[closetTemps.indexOf(nextId)];
      swapDivElements(photo1, photo2);
    }
  }
};

var deleteClosetItem = function(itemId) {
  if (window.confirm("Are you sure you want to delete this item?")) {
    $.ajax({
      type: "POST",
      url: "/delete_closet_item/",
      data: {item_id: itemId},
      success: function(result) {
        window.location.href = '/profile/'
      }
    });
  }
};


$(document).ready(function() {
  //products page order by change event
  $(function() {
    $('#products-filter-select').change(function() {
      $('#products-form').submit();
    });
  });

  $('.pgwSlider').pgwSlider();
  $(function() {
    $('#home-filter').click(function() {
      category = $('#home-filter-category').val();
      type = $('#home-filter-type').val();
      if(category == 'All' && type == 'All') {
        window.location.href = '/products/';
      } else if(category == 'All') {
        window.location.href = '/products/?types='+type;
      } else if(type == 'All') {
        window.location.href = '/products/?categories='+category;
      } else {
        window.location.href = '/products/?categories='+category+'&types='+type;
      }
    });
  });

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
    let firstName = $('#id_first_name').val();
    let lastName = $('#id_last_name').val();
    let bio = $('#id_bio').val();
    let onOffCampus = $('#id_on_off_campus').val();
    let profilePicture = $('#id_profile_picture').val();
    $(window).on("beforeunload", function() {
      if(editProfileFormTouched(firstName, lastName, bio, onOffCampus, profilePicture)) {
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

  if (location.pathname.substring(1) == "edit_closet_item/") {
    let name = $('#id_name').val();
    let category = $('#id_category').val();
    let tradeOptions = $('#id_trade_options').val();
    let price = $('#id_price').val();
    let description = $('#id_description').val();
    let condition = $('#id_condition').val();
    let image1 = $('#temp-image1').val();
    let image2 = $('#temp-image2').val();
    let image3 = $('#temp-image3').val();
    let image4 = $('#temp-image4').val();
    let image5 = $('#temp-image5').val();
    $(window).on("beforeunload", function() {
      if(editItemTouched(name, category, tradeOptions, price, description, condition, image1, image2, image3, image4, image5)) {
        console.log('triggered!');
        return 'Are you sure you want to leave?'; // custom alert messages are no longer supported in most browsers :(
      }
    });
    //turn off the beforeunload event upon form submission
    $(document).ready(function() {
      $("#add-closet-item-form").on("submit", function(e) {
        $(window).off("beforeunload");
        return true;
      });
    });
    //enable / disable the price field
    dropChoice = $('#id_trade_options option:selected').text();
    if(dropChoice == 'Cash Only') {
      $('.add-item-price').css('display', 'flex');
    } else {
      $('.add-item-price').css('display', 'none');
    }
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
      $('.add-item-price').css('display', 'flex');
    } else {
      $('.add-item-price').css('display', 'none');
    }
});

  // --- ADD CLOSET ITEM EVENTS --------------------------------------------------------------------------

  // ---- These functions show photo previews in add closet itm
  closetPhotos = ['picture1', 'picture2', 'picture3', 'picture4', 'picture5'];
  closetFiles = ['id_image1', 'id_image2', 'id_image3', 'id_image4', 'id_image5'];
  closetTemps = ['temp-image1', 'temp-image2', 'temp-image3', 'temp-image4', 'temp-image5']

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
      $('#add_closet_img1').attr('src', addClosetItemDefaultImage);
      $('#id_image1').val('');
      $('#temp-image1').val('');
      $('#picture1').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img2').click(function() {
      $('#add_closet_img2').attr('src', addClosetItemDefaultImage);
      $('#id_image2').val('');
      $('#temp-image2').val('');
      $('#picture2').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img3').click(function() {
      $('#add_closet_img3').attr('src', addClosetItemDefaultImage);
      $('#id_image3').val('');
      $('#temp-image3').val('');
      $('#picture3').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img4').click(function() {
      $('#add_closet_img4').attr('src', addClosetItemDefaultImage);
      $('#id_image4').val('');
      $('#temp-image4').val('');
      $('#picture4').css('display', 'none');
      showAddPhotoButton();
      shuffle();
    });
  });

  $(function() {
    $('#close_img5').click(function() {
      $('#add_closet_img5').attr('src', addClosetItemDefaultImage);
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
        for(var i=0; i<closetPhotos.length; i++) {
          var currentId = '#'+closetPhotos[i];
          if($(currentId).css('display') == 'none') {
            $(currentId).css('display', 'block');
            $('#'+closetFiles[i]).trigger('click');
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
  // --------------- END OF WISHLIST FUNCTIONS ------------------------
});
