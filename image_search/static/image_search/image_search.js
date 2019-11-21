function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#profile-img-tag').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
$("#profile-img").change(function(){
    readURL(this);
    let fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);
});

function upload(event) {
    event.preventDefault();
    var data = new FormData($('#image_form').get(0));
    $.ajax({
        url: 'image_upload',
        type: 'POST',
        data: data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data) {
            // $('#image_form')[0].reset();
            alert('success');
        }
    });
    return false;
}

$(function() {
    $('#image_form').submit(upload);
});