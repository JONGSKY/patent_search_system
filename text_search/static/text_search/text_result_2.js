//// 검색결과

function format(d) {
    return '<h5>Abstract</h5>' + d.abstract + '<br>';
//        '<h5 style="display: inline;">Title</h5>: '+d.title+'<br>'+
}

// 키워드 + 추가키워드로 검색결과 확인하기
$('#search_patent').click(function () {
    var keywords = $('#search_keyword').val().trim();
    $("input[name=add_keyword]").each(function (idx) {
        var add_keyword = $("input[name=add_keyword]:eq(" + idx + ")").val().trim();
        if (add_keyword !== "") {
            keywords = keywords + " " + add_keyword;
        }
    });
    if (keywords === "") {
        alert('검색어를 입력 후 검색해주세요!');
    } else {
        $.ajax({
            method: "GET",
            url: 'text_result',
            data: {'keyword': keywords},
            beforeSend: function () {
                $('html').css("cursor", "wait");
                $('#keyword_list').css('display', 'none');
            },
            complete: function () {
                //통신이 완료된 후 처리되는 함수
                $('#keyword_list').css('display', '');
                $('html').css("cursor", "auto");
            },
            success: function (result) {
                console.log(result);
                if (result === "") {
                    alert(' 죄송합니다. \n 해당 검색어로는 result 결과물이 없습니다! \n 다른 검색어로 검색해주세요');
                } else {
                    $('#wordcloud_section').css('display', 'none');
                    $('#result_section').css('display', 'block');
                    $('#result_pagination').css('display', 'block');
                    $('#search_keyword').val(keywords);
                    $('#keyword_list').empty();
                    // $("#accordion").empty();
                    $("#cloud_s").remove();
                    $("#result_table_wrapper").remove();

                    $('#result_div').append(
                        "<table id=\"result_table\" class=\"display\" style=\"width:100%\">\n" +
                        "            <thead>\n" +
                        "            <tr>\n" +
                        "                <th></th>\n" +
                        "                <th>patent_id</th>\n" +
                        "                <th>title</th>\n" +
                        "                <th>country</th>\n" +
                        "                <th>date</th>\n" +
                        "                <th>site</th>\n" +
                        "            </tr>\n" +
                        "            </thead>\n" +
                        "            <tfoot>\n" +
                        "            <tr>\n" +
                        "                <th></th>\n" +
                        "                <th>patent_id</th>\n" +
                        "                <th>title</th>\n" +
                        "                <th>country</th>\n" +
                        "                <th>date</th>\n" +
                        "                <th>site</th>\n" +
                        "            </tr>\n" +
                        "            </tfoot>\n" +
                        "        </table>"
                    );

                    var dt = $('#result_table').DataTable({
                        // destroy: true,
                        data: result['data_list'],
                        columns: [
                            {
                                "class": "details-control",
                                "orderable": false,
                                "data": null,
                                "defaultContent": ""
                            },
                            {data: 'patent_id'},
                            {data: 'title'},
                            {data: 'country'},
                            {data: 'date'},
                            {
                                data: "country",
                                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                                    $(nTd).html("<a target='_blank' href='http://patents.google.com/patent/" + oData.country + oData.number + oData.kind + "'>Info</a>");
                                }
                            }
                        ],
                        "order": [[1, 'asc']]
                    });

                    // Array to track the ids of the details displayed rows
                    var detailRows = [];
                    $('#result_table tbody').on('click', 'tr td.details-control', function () {
                        var tr = $(this).closest('tr');
                        var row = dt.row(tr);
                        var idx = $.inArray(tr.attr('id'), detailRows);

                        if (row.child.isShown()) {
                            tr.removeClass('details');
                            row.child.hide();

                            // Remove from the 'open' array
                            detailRows.splice(idx, 1);
                        } else {
                            tr.addClass('details');
                            row.child(format(row.data())).show();

                            // Add to the 'open' array
                            if (idx === -1) {
                                detailRows.push(tr.attr('id'));
                            }
                        }
                    });

                    // On each draw, loop over the `detailRows` array and show any child rows

                    dt.on('draw', function () {
                        $.each(detailRows, function (i, id) {
                            $('#' + id + ' td.details-control').trigger('click');
                        });
                    });


                    $(document).ready(function () {

                        /* Column별 검색기능 추가 */
                        $('#result_table_filter').prepend('<select id="select"></select>');
                        $('#result_table > thead > tr').children().each(function (indexInArray, valueOfElement) {
                            if (indexInArray == 0 | indexInArray == 5) {
                            } else {
                                $('#select').append('<option>' + valueOfElement.innerHTML + '</option>');
                            }
                        });

                        $('.dataTables_filter input').unbind().bind('keyup', function () {
                            var colIndex = document.querySelector('#select').selectedIndex + 1;
                            dt.column(colIndex).search(this.value).draw();
                        });

                    });

                    var offset = $("#result_section").offset();
                    $('html, body').animate({scrollTop: offset.top}, 400);


// console.log(result['patent_id_list'].slice(1, 10));

                    // set the dimensions and margins of the graph
                    var margin = {top: 10, right: 30, bottom: 30, left: 60},
                        width = 800 - margin.left - margin.right,
                        height = 600 - margin.top - margin.bottom;

// append the svg object to the body of the page
                    var svg = d3.select("#my_dataviz")
                        .append("svg")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform",
                            "translate(" + margin.left + "," + margin.top + ")");

//Read the data

                    $.ajax({
                        method: "GET",
                        dataType : "json",
                        url: 'clustering_map',
                        // data: {'patent_id': JSON.stringify(result['patent_id_list'].slice(1, 5000)) },
                        // data: "",
                        beforeSend: function () {
                            $('html').css("cursor", "wait");
                            // $('#keyword_list').css('display', 'none');
                        },
                        complete: function () {
                            //통신이 완료된 후 처리되는 함수
                            // $('#keyword_list').css('display', '');
                            $('html').css("cursor", "auto");
                        },
                        success: function (result) {
                            var data = result['xy'];
                            var axis = result['axis'];
                            //    clustering 과정
                            // alert(data['x_value']);
                            //
                            // var obj =  $.parseJSON(data);
                            //     var obj_1 = eval(data);
                            //     alert(obj);
                            //     var obj_2 = JSON.parse(data);
                            //     alert(obj_2);
                            //     console.log(jQuery.type(obj));
                            //     console.log(obj);
                            //     console.log(jQuery.type(obj_2));

                            // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/iris.csv", function (data) {
                            //     console.log(data);
                            // Add X axis
                            var x = d3.scaleLinear()
                                // .domain([10, 100])
                                .domain([axis['s_x']-10, axis['b_x']+10])
                                .range([0, width]);
                            svg.append("g")
                                .attr("transform", "translate(0," + height + ")")
                                .call(d3.axisBottom(x));

                            // Add Y axis
                            var y = d3.scaleLinear()
                                .domain([axis['s_y']-10, axis['b_y']+10])
                                .range([height, 0]);
                            svg.append("g")
                                .call(d3.axisLeft(y));

                            // Color scale: give me a specie name, I return a color

                            const color = d3.scaleOrdinal()
                                .domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                                .range(["#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8", "#636e72"]);


                            // Highlight the specie that is hovered
                            var highlight = function (d) {
                                selected_specie = d.cluster;

                                d3.selectAll(".dot")
                                    .transition()
                                    .duration(100)
                                    .style("fill", "lightgrey")
                                    .attr("r", 3);

                                d3.selectAll("." + selected_specie)
                                    .transition()
                                    .duration(100)
                                    .style("fill", color(selected_specie))
                                    .attr("r", 7)
                            };

                            // Highlight the specie that is hovered
                            var doNotHighlight = function () {
                                d3.selectAll(".dot")
                                    .transition()
                                    .duration(100)
                                    .style("fill", function (d) {
                                            return color(d.cluster)
                                        }
                                    )
                                    .attr("r", 5)
                            };

                            // Add dots
                            svg.append('g')
                                .selectAll("dot")
                                .data(data)
                                .enter()
                                .append("circle")
                                // .attr("name", function (d) {
                                //     return "clustering_" + d.Species
                                // })
                                .attr("class", function (d) {
                                    return "dot " + d.cluster
                                })
                                .attr("cx", function (d) {
                                    // alert(d.Sepal_Length);
                                    return x(d.x_value);
                                })
                                .attr("cy", function (d) {
                                    return y(d.y_value);
                                })
                                .attr("r", 5)
                                .style("fill", function (d) {
                                    return color(d.cluster)
                                })
                                .on("mouseover", highlight)
                                .on("mouseleave", doNotHighlight)

                            // .on("click", function (d) {
                            //     alert(d.Species);
                            //
                            //     $.ajax({
                            //         method: "GET",
                            //         url: 'text_result',
                            //         data: {'keyword': keywords},
                            //         beforeSend: function () {
                            //             $('html').css("cursor", "wait");
                            //             $('#keyword_list').css('display', 'none');
                            //         },
                            //         complete: function () {
                            //             //통신이 완료된 후 처리되는 함수
                            //             $('#keyword_list').css('display', '');
                            //             $('html').css("cursor", "auto");
                            //         },
                            //         success: function (data) {
                            //
                            //
                            //         }
                            //     })
                            //
                            // })
                            // })
                            //    여기까
                        }
                    })
                }
            }
        })
    }
});



















// //// 검색결과
//
// function format(d) {
//     return '<h5>Abstract</h5>' + d.abstract + '<br>';
// //        '<h5 style="display: inline;">Title</h5>: '+d.title+'<br>'+
// }
//
// // 키워드 + 추가키워드로 검색결과 확인하기
// $('#search_patent').click(function () {
//     var keywords = $('#search_keyword').val().trim();
//     $("input[name=add_keyword]").each(function (idx) {
//         var add_keyword = $("input[name=add_keyword]:eq(" + idx + ")").val().trim();
//         if (add_keyword !== "") {
//             keywords = keywords + " " + add_keyword;
//         }
//     });
//     if (keywords === "") {
//         alert('검색어를 입력 후 검색해주세요!');
//     } else {
//         $.ajax({
//             method: "GET",
//             url: 'text_result',
//             data: {'keyword': keywords},
//             beforeSend: function () {
//                 $('html').css("cursor", "wait");
//                 $('#keyword_list').css('display', 'none');
//             },
//             complete: function () {
//                 //통신이 완료된 후 처리되는 함수
//                 $('#keyword_list').css('display', '');
//                 $('html').css("cursor", "auto");
//             },
//             success: function (data) {
//                 if (data == "") {
//                     alert(' 죄송합니다. \n 해당 검색어로는 result 결과물이 없습니다! \n 다른 검색어로 검색해주세요');
//                 } else {
//                     $('#wordcloud_section').css('display', 'none');
//                     $('#result_section').css('display', 'block');
//                     $('#result_pagination').css('display', 'block');
//                     $('#search_keyword').val(keywords);
//                     $('#keyword_list').empty();
//                     // $("#accordion").empty();
//                     $("#cloud_s").remove();
//                     $("#result_table_wrapper").remove();
//
//                     $('#result_div').append(
//                         "<table id=\"result_table\" class=\"display\" style=\"width:100%\">\n" +
//                         "            <thead>\n" +
//                         "            <tr>\n" +
//                         "                <th></th>\n" +
//                         "                <th>patent_id</th>\n" +
//                         "                <th>title</th>\n" +
//                         "                <th>country</th>\n" +
//                         "                <th>date</th>\n" +
//                         "                <th>site</th>\n" +
//                         "            </tr>\n" +
//                         "            </thead>\n" +
//                         "            <tfoot>\n" +
//                         "            <tr>\n" +
//                         "                <th></th>\n" +
//                         "                <th>patent_id</th>\n" +
//                         "                <th>title</th>\n" +
//                         "                <th>country</th>\n" +
//                         "                <th>date</th>\n" +
//                         "                <th>site</th>\n" +
//                         "            </tr>\n" +
//                         "            </tfoot>\n" +
//                         "        </table>"
//                     );
//
//                     var dt = $('#result_table').DataTable({
//                         // destroy: true,
//                         data: data,
//                         columns: [
//                             {
//                                 "class": "details-control",
//                                 "orderable": false,
//                                 "data": null,
//                                 "defaultContent": ""
//                             },
//                             {data: 'patent_id'},
//                             {data: 'title'},
//                             {data: 'country'},
//                             {data: 'date'},
//                             {
//                                 data: "country",
//                                 "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
//                                     $(nTd).html("<a target='_blank' href='http://patents.google.com/patent/" + oData.country + oData.number + oData.kind + "'>Info</a>");
//                                 }
//                             }
//                         ],
//                         "order": [[1, 'asc']]
//                     });
//
//                     // Array to track the ids of the details displayed rows
//                     var detailRows = [];
//                     $('#result_table tbody').on('click', 'tr td.details-control', function () {
//                         var tr = $(this).closest('tr');
//                         var row = dt.row(tr);
//                         var idx = $.inArray(tr.attr('id'), detailRows);
//
//                         if (row.child.isShown()) {
//                             tr.removeClass('details');
//                             row.child.hide();
//
//                             // Remove from the 'open' array
//                             detailRows.splice(idx, 1);
//                         } else {
//                             tr.addClass('details');
//                             row.child(format(row.data())).show();
//
//                             // Add to the 'open' array
//                             if (idx === -1) {
//                                 detailRows.push(tr.attr('id'));
//                             }
//                         }
//                     });
//
//                     // On each draw, loop over the `detailRows` array and show any child rows
//
//                     dt.on('draw', function () {
//                         $.each(detailRows, function (i, id) {
//                             $('#' + id + ' td.details-control').trigger('click');
//                         });
//                     });
//
//
//                     $(document).ready(function () {
//
//                         /* Column별 검색기능 추가 */
//                         $('#result_table_filter').prepend('<select id="select"></select>');
//                         $('#result_table > thead > tr').children().each(function (indexInArray, valueOfElement) {
//                             if (indexInArray == 0 | indexInArray == 5) {
//                             } else {
//                                 $('#select').append('<option>' + valueOfElement.innerHTML + '</option>');
//                             }
//                         });
//
//                         $('.dataTables_filter input').unbind().bind('keyup', function () {
//                             var colIndex = document.querySelector('#select').selectedIndex + 1;
//                             dt.column(colIndex).search(this.value).draw();
//                         });
//
//                     });
//
//                     var offset = $("#result_section").offset();
//                     $('html, body').animate({scrollTop: offset.top}, 400);
//
//                 }
//             }
//         })
//     }
// });