var currShowing = 'poetry';

function upvote() {

    $.ajax({
        url: window.location.pathname + "/upvote", // the endpoint
        type: "POST", // http method
        // handle a successful response
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function (response) {
          //  var value = parseInt($('#upvotes').html());
            //  value += 1;
            //only one key so code surely can be better
            for (key in response) {
                $('#upvotes').html(response[key]);
            }
           
        }

    });
}


function loadData(type) { //we can say we do not care what is the type
    
    //from which location do we want to gather our data, we should who is the user, let's say we know that and what do we want
    //poetry, quotes, stories
    currShowing = type;

    $.ajax({
        url: window.location.pathname + "/" + type, // the endpoint
        type: "POST", // http method
        // handle a successful response
        data: {
            type: type,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },

        success: function (response) {

            typeMap = { "poetry": "poetry", "quotes": "quote", "stories": "story" };

            $('#links').html('');

           // console.log(response);
           // console.log("\n");

            for (key in response) {
                //console.log(key);
                //console.log(response[key]);

                $('#links').append('<a href="/look/' + typeMap[type] + '/' + response[key]['id'] + '"> ' + response[key]['title'] + '</a> &nbsp; &nbsp;');
            }

        }

    });

}


function toArray(obj) {
    var array = [];

    for (var i = obj.length >>> 0; i--;) {
        array[i] = obj[i];
    }
    return array;
}


function linkDateSort() {
    loadData(currShowing);
}

/*
So problem was that our object was not array, great javascript!
*/
function linkSort() {
    
    var links = document.getElementById('links').children;
    links = toArray(links);

    
    links.sort( function(a,b) {
        var t1 = a.innerHTML;
        var t2 = b.innerHTML;
        if (t1 > t2) {
            return 1;
        }
        else if (t2 > t1) {
            return -1;
        }
        else {
            return 0;
        }
    });
    
    $('#links').html('');
  
    for (var i = 0, l = links.length; i < l; i++) {
        $('#links').append(links[i]);
        $('#links').append('&nbsp; &nbsp;')
    }

}




$(document).ready(function () {
    $(".b1").click(function () {
        $(".text1").css("font-weight", "bold");
        $(".text2").css("font-weight", "normal");
        $(".text3").css("font-weight", "normal");
    });

    $(".b2").click(function () {
        $(".text1").css("font-weight", "normal");
        $(".text2").css("font-weight", "bold");
        $(".text3").css("font-weight", "normal");
    });

    $(".b3").click(function () {
        $(".text1").css("font-weight", "normal");
        $(".text2").css("font-weight", "normal");
        $(".text3").css("font-weight", "bold");
    });
});


/* currently not used and not working -> could make 8 functions and each website calls its own to bold it*/

function makeBold(){

    $(".l1").click(function () {
        $(".g1").css("font-weight", "bold");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l2").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "bold");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l3").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "bold");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l4").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "bold");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l5").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "bold");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l6").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "bold");
        $(".g7").css("font-weight", "normal");
        $(".g8").css("font-weight", "normal");
    });

    $(".l7").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "bold");
        $(".g8").css("font-weight", "normal");
    });

    $(".l8").click(function () {
        $(".g1").css("font-weight", "normal");
        $(".g2").css("font-weight", "normal");
        $(".g3").css("font-weight", "normal");
        $(".g4").css("font-weight", "normal");
        $(".g5").css("font-weight", "normal");
        $(".g6").css("font-weight", "normal");
        $(".g7").css("font-weight", "bold");
        $(".g8").css("font-weight", "normal");
    });

}



$(document).ready(function () {

    $(".pub").click(function () {
        $(".pub").css("border", "#000000");
        $(".pub").css("border-style", "solid");
        $(".pub").css("border-width", "3px");
        $(".draft").css("border", "none");

    });

    $(".draft").click(function () {
        $(".draft").css("border", "#000000");
        $(".draft").css("border-style", "solid");
        $(".draft").css("border-width", "3px");
        $(".pub").css("border", "none");
       
    });

});

var cnt = 0;

$(function() {
    $("#add").click(function() {
        if ($("#add").val() == "Quote" && cnt == 0) {
            cnt = 1;

            $(".inner").append("<br>");


            var boxElement = $('<input>').attr({
                name: "originalauthor", class: "form-control", id: "noticeweeks", placeholder: " Original source (can be unknown): "
            });
           // "<br>".appendTo("#inputplace");
            // "Source (can be unknown)".appendTo("#inputplace");
            boxElement.appendTo("#inputplace");

         //   $("#add").val("Notice me in...");
        }
    });
});

$(function () {
    $(".remove").click(function () {
        cnt = 0;
        $(".inner").empty();
    });
});