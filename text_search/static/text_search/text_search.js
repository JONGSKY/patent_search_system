// 워드클라우드

// 워드클라우드 검색어로 생성하기
$('#submit_keyword').click(function(){
    var keywords = $('#search_keyword').val().trim();
    if (keywords === ""){
        alert('검색어를 입력 후 검색해주세요!');
    } else {
        $.ajax({
            method: "GET",
            url: 'wordcloud',
            data: {'keyword': keywords},
            beforeSend: function() {
            $('html').css("cursor","wait");
            },
            complete: function() {
            $('html').css("cursor","auto");
            },
            success: function (data) {
                myWords = data['myWords'];
                if (myWords == ""){
                    alert(' 죄송합니다. \n 해당 검색어로는 wordcloud 제작이 어렵습니다! \n 다른 검색어로 검색해주세요');}
                    else {
                    $('#result_section').css('display', 'none');
                    $('#result_pagination').css('display', 'none');
                    $('#wordcloud_section').css('display', 'block');
                    createWordCloud(myWords);
                    }
            }
        })
    }
});

// 워드클라우드 변수 지정
var margin = {top: 10, right: 10, bottom: 10, left: 10}
var width = 568 - margin.left - margin.right;
var height = 450 - margin.top - margin.bottom;
var myWords;
var svg = d3.select("#wordcloud_svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var layout = d3.layout.cloud().size([width, height]);

// 워드클라우드 생성 함수
function createWordCloud(myWords){
    $("#cloud_s").remove();
    layout = layout.words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
        .padding(5)        //space between words
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) { return d.size; })      // font size of words
        .on("end", draw);
    layout.start();
}

// 워드클라우드 그리기 힘수
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
            var keyword_tag = '<div class="col-xs-1 form-inline add_keyword_group">' +
                '<input name="add_keyword" class="form-control keywords" style="background-color:#D9E5FF; color:#6799FF; margin:10px 5px 10px 5px" type="text" value=' + ctr +'>' +
                '<div class="input-group-append div_add_keyword"><button class="btn btn-primary button_add_keyword" type="button"><i class="fa fa-times"></i></button></div>';

            var keyword_tag = '<div class="input-group form-inline col-3 add_keyword_group" style="margin-top: 5px;">\n' +
                '    <input type="text" name="add_keyword" class="form-control keywords" value="'+ ctr + '">\n' +
                '    <div class="input-group-append div_add_keyword">\n' +
                '      <button class="btn btn-danger button_add_keyword" type="button"><i class="fa fa-times"></i></button>  \n' +
                '     </div>\n' +
                '  </div>';

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

// 추가 키워드 제거 후 워드클라우드 재생성
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










// 검색결과

// 키워드 + 추가키워드로 검색결과 확인하기
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
            beforeSend: function() {
            $('html').css("cursor","wait");
            },
            complete: function() {
            //통신이 완료된 후 처리되는 함수
            $('html').css("cursor","auto");
            },
            success: function (data) {
                if (data == ""){
                    alert(' 죄송합니다. \n 해당 검색어로는 result 결과물이 없습니다! \n 다른 검색어로 검색해주세요');}
                    else {
                $('#wordcloud_section').css('display', 'none');
                $('#result_section').css('display', 'block');
                $('#result_pagination').css('display', 'block');
                $('#search_keyword').val(keywords);
                $('#keyword_list').empty();
                $("#accordion").empty();
                $("#cloud_s").remove();

                $.each(data, function(key, value) {
                    var link_url = "http://patents.google.com/patent/" + value.country + value.number + value.kind;
                    var title_button = '<button id="clickme" class="btn btn-link" type="button" data-target="#collapse_'+ key + '">'
                        + value.number + '  ' + value.title + '</button>';
                    var link_button = '<button class="btn btn-secondary" type="button" style="float: right;" ' + 'onclick="' +
                        'window.open(\'' + link_url + '\')">자세히 보기 <i class="fa fa-paper-plane" aria-hidden="true"></i></button>';
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
          }
        })
    }
});

// 버튼 클릭시 자세하게 볼 수 있게 열리기
$(document).on("click", "button", function(){
    var target = $(this).attr('data-target');
        $(target ).slideToggle( "slow", function() {
    });
});

// 전체 열기
$(document).on("click", "#all_open", function(){
    for(var i=0; i<9; i++){
    var target = "#collapse_"+i;
    $(target).slideDown("slow", function() {
        // Animation complete.
    });
    }
});

// 전체 닫기
$(document).on("click", "#all_close", function(){
    for(var i=0; i<9; i++){
    var target = "#collapse_"+i;
    $(target).slideUp("slow", function() {
        // Animation complete.
    });
    }
});