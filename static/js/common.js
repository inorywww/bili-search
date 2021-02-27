$(function () {
    // 显示历史
    $("#search-keyword").mousedown(function () {
        if ($('#search-keyword').val() === "") {
            show_history();
        }
        if ($('#search-keyword').val() !== "") {
            $(".suggest-wrap").css("display", "block");
            search_prompt();
        }
    });

    // 搜索提示
    $("#search-keyword").keyup(function (e) {
        if ($('#search-keyword').val() === "") {
            show_history()
        } else {
            search_prompt();
        }
    });

    //点击空白地方隐藏
    $(document).click(function (e) {
        var _con = $('.suggest-wrap,#search-keyword');   // 设置目标区域</span>
        if (!_con.is(e.target) && _con.has(e.target).length === 0) {
            $(".suggest-wrap").css("display", "none")
            // 功能代码
        }
    });

    // 搜索提示
    function search_prompt() {
        let data = {};
        data['keyword'] = $('#search-keyword').val();
        console.log(data);
        $.ajax(
            {
                url: "/prompt",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (res) {
                    if (res !== "undefined" && data['keyword'] !== "") {
                        console.log("success");
                        show_prompt(res)
                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    }

    // 搜索提示显示
    function show_prompt(res) {
        console.log(res.length);
        if (res.length === 0) {
            $(".suggest-wrap").css("display", "none");
            return
        }
        if ($(".suggest-wrap").css("display") === "none") {
            $(".suggest-wrap").css("display", "block");
        }
        for (let i = 0; i < $(".keyword-wrap li").length; i++) {
            if ($(".keyword-wrap li").eq(i).css("display") === "none") {
                $(".keyword-wrap li").eq(i).css("display", "block")
            }
        }
        for (let i = 0; i < res.length; i++) {
            $(".vt-text").eq(i).text("");
            let h = $.parseHTML(res[i]['highlight']);
            $(".vt-text").eq(i).append(h);
        }
    }

    // 显示历史
    function show_history() {
        if ($(".suggest-wrap").css("display") === "none") {
            $(".suggest-wrap").css("display", "block");
        }
        $.ajax(
            {
                url: "/history",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify({}),
                contentType: 'application/json; charset=UTF-8',
                success: function (res) {
                    if (res !== "undefined") {
                        console.log("success");
                        console.log(res);
                        for (let i = 0; i < res.length; i++) {
                            $(".vt-text").eq(i).text(res[i]['his']);
                        }
                        for (let i = res.length; i < 10; i++) {
                            $(".keyword-wrap li").eq(i).css("display", "none");
                            $(".keyword-wrap li a").eq(i).text("");
                        }
                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    }
});