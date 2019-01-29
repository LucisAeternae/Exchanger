$('#login_ajax').on('submit', function(event) {
  event.preventDefault();
  signin();
}); 
$("#close").click(function() {
  $('#results').hide();
});

function signin() {
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.post({
    url: '/signin_ajax/',
    data: {
      username: $('#username').val(),
      password: $('#password').val(),
      csrfmiddlewaretoken: csrftoken
    },
    dataType: 'json',
    success: function(data) {
      var $containers = $('.notloggedin');
      console.log(data.username)
      $(".notloggedin").load(" .notloggedin");
      $(".notloggedin2").load(" .notloggedin2");
    },
    error: function(xhr, errmsg, err, json) {
      $('#results').show();
      $('#results').html("<div class='alert alert-warning' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' id='close' class='close'>&times;</a></div>");
      $("#close").click(function() {
        $('#results').hide();
      });
    }
  });
};
$(document).ready(function() {
  $('#search').keyup(function() {
    var query;
    query = $(this).val();
    $.get('/search/', {
      suggestion: query
    }, function(data) {
      $('#search_field').html(data);
    });
  });
});
$(document).ready(function() {
  $('#search').focusin(function() {
    $('#search_field').show();
  });
});
$(document).click(function(event) {
  if (!$(event.target).closest('.search_form').length) {
    if ($('#search_field').is(":visible")) {
      $('#search_field').hide();
    }
  }
});
$(document).ready(function() {
  var href = $('.btnblack').attr('onclick')
  $("#quantityrange").mousemove(function() {
    $('.oquantity').text(this.value);
    var s = $(this).attr('data');
    $('.oprice').text(this.value * s);
    var quantity = href.slice(0, -1) + this.value + '/"';
    $('.btnblack').attr('onclick', quantity);
  });
});
$(document).ready(function() {
  $("#id_type").change(function() {
    if ($(this).val() == 'Custom') {
      $("#hidden").removeAttr("style").show();
    }
    if ($(this).val() == 'Base') {
      $("#hidden").hide();
    }
  });
});
$(document).ready(function() {
  $(".active-btn").click(function() {
    var offer = $(this).attr("data");
    var button = $(this).attr("class");
    var object = $(this);
    $("<div>Are you sure?</div>").dialog({
      dialogClass: "no-close",
      buttons: {
        "Yes": function() {
          $.get({
            url: "{% url 'offer_status_change' %}",
            data: {
              "offer": offer,
              "button": button
            },
            dataType: "json",
            success: function(data) {
              if (data.success) {
                if (data.delete) {
                  $(object).parent().parent().hide();
                } else if (data.pause) {
                  if ($(object).attr("class") == "active-btn play-btn") {
                    $(object).attr("class", "active-btn pause-btn");
                  } else {
                    $(object).attr("class", "active-btn play-btn");
                  }
                } else {
                  alert("Error")
                }
              } else {
                alert("Error!")
              }
            }
          })
          $(this).dialog("close");
        },
        "Cancel": function() {
          $(this).dialog("close");
        }
      }
    });
  });
});

$("#close").click(function() {
  $('#results').hide();
});
