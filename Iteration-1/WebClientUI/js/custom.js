$(function () {

  // sorce: http://stackoverflow.com/a/22172860
  function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
  }

  $('.thumbnail img')
    .click(function () {
      var btm_img = $(this).attr('src');
      $('#img_plc').attr('src', btm_img);
      $('#txt_area').hide();
    });

  $("#clk").on('click', function (event) {
    $('#txt_area').hide();
    $('#meow').show();
    var tmp_img = document.createElement("img");
    tmp_img.src = 'http://'+location.host+'/'+$('#img_plc').attr('src'); 
    var base64 = getBase64Image(tmp_img);
    console.log(base64);
    $.ajax({
      type: "POST",
      url: "http://localhost:8080/get_custom",
      data: base64,
      success: function (result) {
        $('#meow').hide();
        $('#txt_area').text(result);
        $('#txt_area').show();
      },
      error: function (xhr, textStatus, error) {
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });
  });
});