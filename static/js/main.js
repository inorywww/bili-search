$(function () {
    // console.log("12340");
    $(".searchBtn").click(function () {
        let data = {};
        data['keyword'] = $('#search-keyword').val();
        console.log(data['keyword']);
        var newwindow = window.open("about:blank");
        newwindow.location = "http://www.baidu.com";

        // window.focus();
        $.ajax({
                url: "/search",
                type: "POST",
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (data) {
                    console.log("search");
                    console.log(data);
                }
            },
            {
                url: "/query",
                type: "POST",
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (data) {
                    console.log("query");
                    console.log(data);
                }
            })
    })
});