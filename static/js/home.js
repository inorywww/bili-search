$(function () {

    // 点击搜索
    $(".searchBtn").click(function () {
        if ($('#search-keyword').val() !== "") {
            search_event($('#search-keyword').val());
        }
    });

    // 回车搜索
    $('#search-keyword').keydown(function (e) {
        if (e.keyCode === 13) {
            if ($('#search-keyword').val() !== "") {
                search_event($('#search-keyword').val());
            }
        }
    });

    //提示搜索
    $(".vt-text").click(function () {
        console.log($(this).text());
        search_event($(this).text());
    });
    //搜索热门
    $(".word ").click(function () {
        list_search($(this).text())
    });

    //搜索历史
    $(".history_btn").click(function () {
        list_search($(this).text())
    });

    // 清除历史
    $(".icon-garbage").click(function(){
         $.ajax(
            {
                url: "/clear_history",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify({}),
                contentType: 'application/json; charset=UTF-8',
                success: function (res) {
                    if (res !== "undefined") {
                        console.log("success");
                        console.log(res);
                        $(".history .list").empty();
                        $(".history .list").css("display","none");
                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    });
    // 热门
    function list_search(keyword) {
        let data = {};
        data['keyword'] = keyword;
        add_history(data['keyword']);
        console.log(data);
        window.focus();
        $.ajax(
            {
                url: "/query",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (o) {
                    if (o !== "undefined" && data['keyword'] !== "") {
                        window.open('/search/?keyword=' + data['keyword']);
                        console.log("query");
                    }
                },
                error: function () {
                    console.log("error");
                }
            },);
    }

    // 搜索事件
    function search_event(keyword) {
        let data = {};
        data['keyword'] = keyword;
        add_history(data['keyword']);
        console.log(data);
        window.focus();
        $.ajax(
            {
                url: "/query",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (o) {
                    if (o !== "undefined" && data['keyword'] !== "") {
                        console.log(window.location.href);
                        window.open('/search/?keyword=' + data['keyword']);
                        console.log("success");

                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    }

     // 添加历史
    function add_history(keyword) {
        let flag = true;
        for (let i = 0; i < $(".history_btn").length; i++) {
            if (keyword === $(".history_btn").eq(i).text()) {
                flag = false;
                break;
            }
        }
        if (flag === true) {
            let li = $("<li class='item'></li>");
            let aa = $("<a href=javascript:; class='history_btn'></a>");
            aa.text(keyword);
            li.append(aa);
            $(".home-wrap .home-suggest .history .list").append(li);
        }
    }
});