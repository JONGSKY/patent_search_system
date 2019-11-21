// // List of words

var margin = {top: 10, right: 10, bottom: 10, left: 10}
var width = 450 - margin.left - margin.right;
var height = 450 - margin.top - margin.bottom;
var myWords;

var svg = d3.select("#wordcloud_svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var layout = d3.layout.cloud().size([width, height]);

function createWordCloud(myWords){
    $("#cloud_s").remove();
    layout = layout.words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
        .padding(5)        //space between words
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) { return d.size; })      // font size of words
        .on("end", draw);
    layout.start();
}

function draw(words) {
    svg.append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .attr("id", "cloud_s")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function(d) { return d.size; })
        .style("fill", "#69b3a2")
        .attr("text-anchor", "middle")
        .style("font-family", "Impact")
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
        .on("click", function(d){
            var ctr = d.text;
            var keyword_tag = '<div class="col-xs-2 form-inline add_keyword_group">' +
                '<input name="add_keyword" class="form-control keywords" style="background-color:#D9E5FF; color:#6799FF; margin:10px 5px 10px 5px" type="text" value=' + ctr +'>' +
                '<div class="input-group-btn div_add_keyword"><button class="btn btn-primary button_add_keyword" type="submit"><i class="fa fa-times"></i></button></div>'
            $('#keyword_list').append(keyword_tag);
            $("#cloud_s").remove();

            for(var i in myWords){
                if(myWords[i].word===d.text){
                    myWords.splice(i,1);}
            }
            var layout = d3.layout.cloud()
                .size([width, height])
                .words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
                .padding(5)        //space between words
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .fontSize(function(d) { return d.size; })      // font size of words
                .on("end", draw);
            layout.start();
        })
    ;
}

$('body').on("click", ".div_add_keyword", function(){
    $(this).parent("div").remove();

    var del_val = $(this).parent("div").children("input").attr('value');
    $("#cloud_s").remove();
    myWords.push({word:del_val, size: "40"});

    var layout = d3.layout.cloud()
        .size([width, height])
        .words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
        .padding(5)        //space between words
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) { return d.size; })      // font size of words
        .on("end", draw);
    layout.start();
});


$('#submit_keyword').click(function(){
    var keywords = $('#search_keyword').val().trim();
    if (keywords === ""){
        alert('검색어를 입력 후 검색해주세요!');
    } else {
        $.ajax({
            method: "GET",
            url: 'wordcloud_search',
            data: {'keyword': keywords},
            success: function (data) {
                myWords = data['myWords'];
                createWordCloud(myWords);
            }
        })
    }
});

$('#search_patent').click(function(){
    var keywords = $('#search_keyword').val().trim();
    $("input[name=add_keyword]").each(function(idx){
        var add_keyword = $("input[name=add_keyword]:eq(" + idx + ")").val().trim();
        if(add_keyword !== ""){
            keywords = keywords + " " + add_keyword;
        }
    });
    if (keywords === ""){
        alert('검색어를 입력 후 검색해주세요!');
    } else {
        $.ajax({
            method: "GET",
            url: 'text_result',
            data: {'keyword': keywords},
            success: function (data) {
                var event_data = '<section class="page-section" id="services_result">'
                    + '<div class="container">'
                    + '<h2 class="text-center mt-0">Result</h2>'
                    + '<hr class="divider my-4">'
                    + '<div class="row">'
                    + '<div class="panel-group" id="accordion">'
                    + '<div>'
                    + '<button id="all_open" class="btn btn-link" type="button"> 전체 열기 </button>'
                    + '<button id="all_close" class="btn btn-link" type="button"> 전체 닫기 </button>'
                    + '</div>';

                $("#accordion").empty();
                $.each(data, function(key, value) {
                    var link_url = "http://patents.google.com/patent/" + value.country + value.number + value.kind;
                    var title_button = '<button class="btn btn-link card-link" data-toggle="collapse" href="#collapse_' + key + '">'
                        + value.number + '  ' + value.title + '</button>';
                    var link_button = '<button class="btn btn-secondary" type="button" style="float: right;" ' + 'onclick="' +
                        'window.open(\'' + link_url + '\')">해당 사이트로 이동 <i class="fa fa-paper-plane" aria-hidden="true"></i></button>';
                    var html = '<div class="card">'
                        + '<div class="card-header">' + title_button + link_button + '</div>'
                        + '<div id="collapse_' + key + '" class="collapse" data-parent="#accordion">'
                        + '<div class="card-body">'
                        + '<div class="row"><h5>&nbsp;Date&nbsp;</h5>:&nbsp;' + value.date + '</div>'
                        + '<div class="row"><h5>&nbsp;Country&nbsp;</h5>:&nbsp;' + value.country + '</div>'
                        + '<div class="row"><h5>&nbsp;Abstract&nbsp; </h5>&nbsp;&nbsp;' + value.abstract + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>';
                    $("#accordion").append(html);
                });
            }
        })
    }
});
