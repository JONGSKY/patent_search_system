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
// append the svg object to the body of the page
//     var svg = d3.select("#wordcloud").append("svg")
//         .attr("width", width + margin.left + margin.right)
//         .attr("height", height + margin.top + margin.bottom)
//         .attr("id", "wordcloud_svg")
//         .append("g")
//         .attr("transform",
//             "translate(" + margin.left + "," + margin.top + ")");
    $("#cloud_s").remove();
//     var layout = d3.layout.cloud()
//         .size([width, height])
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
            var keyword_tag = '<div class="col-xs-2 form-inline add_keyword_group"><input name="add_keyword" class="form-control keywords" style="background-color:#D9E5FF; color:#6799FF; margin:10px 5px 10px 5px" type="text" value=' + ctr +'><div class="input-group-btn div_add_keyword"><button class="btn btn-primary button_add_keyword" type="submit"><i class="fa fa-times"></i></button></div>'
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
                $('#results').html(JSON.stringify(data));
                // alert(JSON.stringify(data));
                // myWords = data['myWords'];
                // createWordCloud(myWords);
            }
        })
    }
});



