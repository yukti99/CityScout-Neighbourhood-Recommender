var nums = 1;

$(document).ready(function () {
  $('select').change(function () {
    $('#preferenceList').empty();
    nums = $('#preferenceNo').val();
    for (let i = 0; i < nums; i++) {
      let formGroup = `<div class='form-group'>\
        <label for='preference${i + 1}'>\
        Preference #${i + 1}</label>\
        <input class='form-control' id='preference${i + 1}' />\
        </div>`;
      $('#preferenceList').append(formGroup);
    }
  });
});

$(document).ready(function () {
  $("#City").focus();
});

$(document).ready(function () {
  $('#input-next-btn').click(function (event) {
    event.preventDefault();
    user_input = getUserInput();
    if (user_input != false){
      loading();
      getGPTResponseForAreas(user_input);
    }
  });
});

function loading() {
  $('.loading').show();
  $('.content').hide();
}

function getUserInput() {
  let city = $.trim($('#City').val());
  let preferences = [];
  console.log(city);
  console.log(nums);
  let error_flag = false;

  for (let i = 0; i < nums; i++) {
    let id = '#preference' + (i + 1).toString();
    let pref = $.trim($(id).val());
    console.log(id);
    console.log(pref);
    // error handling
    if (pref === ""){
      error_flag = true;
      let error_msg = "Please enter Preference #"+(i+1).toString();
      $(id).css("border", "2px solid #ff9494");
      $(id).focus();
      $(id).attr("placeholder", error_msg);
    }else{
      preferences.push(pref);
    }
  }

  // error handling
  if (city === ""){
    error_flag = true;
    let error_msg = "Please enter a city";
    $("#City").css("border", "2px solid #ff9494")
    $("#City").attr("placeholder", error_msg);
    $("#City").focus();
  }

  if (!error_flag){
    user_input = {
      city: city,
      preferences: preferences,
    };
    return user_input;
  }
  return false;
}

function getGPTResponseForAreas(user_input) {
  console.log(user_input);
  let data = {
    user_input: user_input,
  };

  console.log(data);
  console.log(JSON.stringify(data));
  $.ajax({
    type: 'POST',
    url: '/suggested_areas',
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (result) {
      let response_areas = result['gpt_areas'];
      console.log('Response Areas: ', response_areas);
      location.href = 'http://127.0.0.1:3000/areas';
    },
    error: function (request, status, error) {
      console.log('Error Occured during ajax call');
      console.log(request);
      console.log(status);
      console.log(error);
    },
  });
}
