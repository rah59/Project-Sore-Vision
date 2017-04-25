$(function () {

    // sorce: http://stackoverflow.com/a/22172860
    function getBase64Image(img) {
        var canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        var dataURL = canvas.toDataURL("image/jpg");
        return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    }

    $('.thumbnail img')
      .click(function () {
          var btm_img = $(this).attr('src');
          $('#img_plc').attr('src', btm_img);
          $('#txt_area').hide();
          $('#meow').hide();
      });

    $("#clk").on('click', function (event) {
        $('#txt_area').hide();
        $('#meow').show();
        var tmp_img = document.createElement("img");
        //alert($('#img_plc').attr('src'));
        //tmp_img.src = 'http://' + location.host + '/' + $('#img_plc').attr('src');
        //tmp_img.src = 'file:///home/raj/Documents/BigDataSpring2017/SoreVisionInception/WebClientUI/' + $('#img_plc').attr('src');
        tmp_img.src = $('#img_plc').attr('src');
        var base64 = getBase64Image(tmp_img);
        //alert(base64);
        console.log(base64);
        //var imgData = JSON.stringify(base64);
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8080/get_custom",
            //dataType: 'json',
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

    function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#img_plc').attr('src', e.target.result);
                }

                reader.readAsDataURL(input.files[0]);
            }
        }

        $("#imgInp").change(function(){
            readURL(this);
            $('#txt_area').hide();
        });
});
