function upvote() {

    $.ajax({
        url: window.location.pathname + "/upvote", // the endpoint
        type: "POST", // http method
        // handle a successful response
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function (response) {
            var value = parseInt($('#upvotes').html());
            value += 1;
            $('#upvotes').html(value);
        }

    });
}


function loadData(type) { //we can say we do not care what is the type
    
    //from which location do we want to gather our data, we should who is the user, let's say we know that and what do we want
    //poetry, quotes, stories

    $.ajax({
        url: window.location.pathname + "/" + type, // the endpoint
        type: "POST", // http method
        // handle a successful response
        data: {
            type: type,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },

        success: function (response) {

            $('#links').html('');

            for (key in response) {
                $('#links').append('<a href="/look/poetry/' + response.key.id + '"> ' + response.key.title + '</a> &nbsp; &nbsp;');
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
    
    document.getElementById("links").innerHTML = "";
  
    for (var i = 0, l = links.length; i < l; i++) {
        document.getElementById("links").append(links[i]);
        document.getElementById("links").append(" ");
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
                name: "originalAuthor", class: "form-control", id: "noticeweeks", placeholder: " Original source (can be unknown): "
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