function stripHtml(html) {
    let tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

function getWords(id) {
    $('.marked-underlined').each(function (i, obj) {
        obj.classList.remove('marked-active');
    });
    $('.card-synonyms').each(function (i, obj) {
        obj.classList.remove('card-synonyms-active');
    });

    var words = $("#mark-" + id).data('words');
    $('#mark-' + id).addClass('marked-active');

    $("#div-" + id).addClass('card-synonyms-active');

    document.getElementById("div-" + id).scrollIntoView({behavior: 'smooth', block: 'center'});

}

function createSynonymList() {

    $("#synonyms").empty();
    $(".marked-underlined").each(function () {

        var arr = $(this).data('words');
        var text = $(this).html();
        var id = $(this).data('id');

        var div = jQuery('<div>', {
            id: 'div-' + id,
            class: 'card-synonyms',
        });
        var divOrigin = jQuery('<div>', {
            class: 'card-item-origin',
            html: text,
            onclick: 'swapText(' + id + ', "' + text + '")',
        });

        div.append(divOrigin);
        for (var i = 0; i < arr.length; ++i) {
            var divSwap = jQuery('<div>', {
                class: 'card-item-swap',
                html: arr[i],
                onclick: 'swapText(' + id + ', "' + arr[i] + '")',
            });
            div.append(divSwap);
        }
        $('#synonyms').append(div);
        //console.log($(this));
    });
}

function swapText(id, text) {
    document.getElementById("mark-" + id).scrollIntoView({behavior: 'smooth', block: 'center'});
    $('.card-synonyms').each(function (i, obj) {
        obj.classList.remove('card-synonyms-active');
    });

    $('.marked-underlined').each(function (i, obj) {
        obj.classList.remove('marked-active');
    });

    $("#div-" + id).addClass('card-synonyms-active');
    $('#mark-' + id).addClass('marked-active');
    $('#mark-' + id).html(text);
}

$(document).ready(function () {

    var fr = $('#from').redactor({'buttons': ['html', 'bold', 'italic', 'deleted', 'underline', 'link']});
    var to = $('#to').redactor({'buttons': ['html', 'bold', 'italic', 'deleted', 'underline', 'link']});

    $("#check").on("click", function () {
        var text = $("#from").val();
        $("#id_loader").removeClass("hidden");
        $.post("http://localhost:8000/check/", {
            text: text
        })
            .done(function (data) {
                $("#id_loader").addClass("hidden");
                var arr = JSON.parse(data);
                var out = $('.redactor-editor').last().html(arr['html']);
                //$('#synonyms').html(arr['data']);
                window.print(text)

                createSynonymList();
            });
    });

});