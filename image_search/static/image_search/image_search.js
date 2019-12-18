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
        beforeSend : function() {
            $('#results').empty()
        },
        success: function(data) {
            $.each(data, function (index, item) {
                var card_front = '<div class="col-md-3 col-sm-6 thumbnail-card">' +
                    '<div class="card card-flip h-100">' +
                    '<div class="card-front">' +
                    '<div class="card-body">' +
                    '<img class="card-image" src="/media/' + item.image_src +'" onerror="this.onerror=null; this.src=\'/static/image_search/images/default.png\'">\n' +
                    '<hr>\n' +
                    '<h5 class="card-title">Patent ID : ' + item.patent_id + '</h5>\n' +
                    '</div>\n' +
                    '</div>';

                var card_back = '<div class="card-back bg-white">\n' +
                    '<div class="card-body">\n' +
                    '<h6 class="card-title">' + item.title + '</h6>\n' +
                    '<hr>\n' +
                    '<p class="card-text">' + item.abstract.slice(0, 230 - item.title.length) + '...' + '</p>\n' +
                    '<hr>\n' +
                    '<a target="_blank" href="http://patents.google.com/patent/US' + item.patent_id + '" class="btn btn-primary">Google Patents</a>\n' +
                    '</div>\n' +
                    '</div>\n' +
                    '</div>\n' +
                    '</div>';

                $('#results').append(card_front + card_back);
            });
        }
    });
    return false;
}

$(function() {
    $('#image_form').submit(upload);
});
