$(function (forcedReload) {
    $(".pagination-btn").eq(0).css({
        'background': '#00a1d6',
        'color': '#fff'
    });
    console.log($(".video-item").length);
    if ($(".video-item").length < 20) {
        $(".pager").css('display', 'none')
    } else {
        $(".pager").attr("style", null);
    }

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

    $(".filter-item").click(function () {
        // 点切换样式
        $(this).addClass('active');
        $(this).siblings().removeClass('active');
        $(".pagination-btn").eq(0).css({
            'background': '#00a1d6',
            'color': '#fff'
        });
        $(".back-btn").parent().css('display', 'none');
        // $(".pagination-btn").eq(0).parent().siblings().children().attr("style", null);

        //获取 综合排序 最多点击 最新发布 其中有一个
        let view_items = $(".order li");
        let view_way = '';
        let keyword = $('#search-keyword').val();

        for (let i = 0; i < view_items.length; i++) {
            if (view_items.eq(i).is('.active')) {
                if (i === 0) {
                    view_way = ''
                } else if (i === 1) {
                    view_way = 'view'
                } else if (i === 2) {
                    view_way = "pubdate"
                }
                break;
            }
        }

        // 获取 全部时长 10分钟以下 10-30分钟 30-60分钟 60分钟以上 其中一个
        let time_items = $(".duration li");
        let start_time = 0;
        let end_time = 0;

        for (let i = 0; i < time_items.length; i++) {
            if (time_items.eq(i).is('.active')) {
                if (i === 0) {
                    start_time = 0;
                    end_time = 0;
                } else if (i === 1) {
                    start_time = 0;
                    end_time = 10;
                } else if (i === 2) {
                    start_time = 10;
                    end_time = 30;
                } else if (i === 3) {
                    start_time = 30;
                    end_time = 60;
                } else if (i === 4) {
                    start_time = 60;
                    end_time = 600;
                }
                break;
            }
        }
        time_event(keyword, view_way, start_time, end_time)
    });

    //跳转页面
    $(".pagination-btn").click(function () {
        //去掉上一页btn
        if ($(this).text() === '1') {
            $(".next-btn").parent().css('display', 'inline-block');
        } else if ($(this).text() === ($(".pagination-btn").length).toString()) {
            $(".next-btn").parent().css('display', 'none');
        } else {
            $(".next-btn").parent().css('display', 'inline-block');
        }
        $(this).css({
            'background': '#00a1d6',
            'color': '#fff'
        });
        $(this).parent().siblings().children().attr("style", null);
        let page_num = $(this).text();
        turn_page(parseInt(page_num) - 1)
    });

    // 上一页
    $(".back-btn").click(function () {
        let pb = $(".pagination-btn");
        for (let i = 0; i < pb.length; i++) {
            if (pb.eq(i).attr('style')) {
                // 如果上一页是第一页 就隐藏上一页的btn
                if (i - 1 === 0) {

                    $(".next-btn").parent().css('display', 'inline-block');
                } else {
                    // $(".back-btn").parent().css('display', 'inline-block');
                    $(".next-btn").parent().css('display', 'inline-block');
                }
                pb.eq(i - 1).css({
                    'background': '#00a1d6',
                    'color': '#fff',
                });
                pb.eq(i - 1).parent().siblings().children().attr("style", null);
                turn_page(i - 1);
                break;
            }
        }
    });

    //下一页
    $(".next-btn").click(function () {
        let pb = $(".pagination-btn");
        for (let i = 0; i < pb.length; i++) {
            if (pb.eq(i).attr('style')) {
                // 如果下一页是第十页 就隐藏下一页的btn
                if (i + 1 === pb.length - 1) {
                    $(".next-btn").parent().css('display', 'none');
                    // $(".back-btn").parent().css('display', 'inline-block');
                } else {
                    $(".back-btn").parent().css('display', 'inline-block');
                    // $(".next-btn").parent().css('display', 'inline-block');
                }
                pb.eq(i + 1).css({
                    'background': '#00a1d6',
                    'color': '#fff',
                });
                $(".pagination-btn").eq(i + 1).parent().siblings().children().attr("style", null);
                turn_page(i + 1);
                break;
            }
        }

    });

    //翻页请求数据
    function turn_page(page_num) {
        let data = {};
        data['keyword'] = $('#search-keyword').val();
        data['page_num'] = page_num.toString();
        console.log(data);
        $.ajax(
            {
                url: "/page",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (res) {
                    if (res !== "undefined" && data['keyword'] !== "") {
                        window.history.pushState({}, 0, '/search/?keyword=' + data['keyword'] + '&page=' + (parseInt(data['page_num']) + 1).toString());
                        console.log("success");
                        page(res)
                    }
                },
                error: function () {
                    console.log("error");
                }
            },);
    }

    //搜索事件
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
                        window.location.href = ('/search/?keyword=' + data['keyword']);
                        console.log("success");
                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    }

    // 根据时长筛选事件
    function time_event(keyword, view_way, start_time, end_time) {
        let data = {};
        data['keyword'] = keyword;
        data['view_way'] = view_way;
        data['start_time'] = start_time;
        data['end_time'] = end_time;
        console.log(data);
        $.ajax(
            {
                url: "/view_time",
                type: "POST",
                //async: false,
                dataType: "json",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8',
                success: function (res) {
                    if (res !== "undefined" && data['keyword'] !== "") {
                        console.log("success");
                        page(res);
                    }
                },
                error: function () {
                    console.log("error");
                }
            },
        );
    }

    //重新渲染
    function page(res) {
        console.log(res);

        // 先让全部video显示
        for (let i = 0; i < 20; i++) {
            $(".img-anchor").eq(i).parent().attr('style', null);
        }

        // 改变有的video的属性
        for (let i = 0; i < res.length; i++) {
            $(".img-anchor").eq(i).attr('href', res[i]['href']);
            $(".img img").eq(i).attr('src', res[i]['pic']);
            $(".img .so-imgTag_rb").eq(i).text(res[i]['duration']);

            $(".info .headline .title").eq(i).attr('href', res[i]['href']);
            $(".info .headline .title").eq(i).empty();
            let h = $.parseHTML(res[i]['highlight']);
            $(".info .headline .title").eq(i).append(h);
            let ii1 = $("<i class='icon-playtime'></i>");
            $(".info .tags .watch-num").eq(i).text(res[i]['view']);
            $(".info .tags .watch-num").eq(i).append(ii1);
            let ii2 = $('<i class="icon-date" style="float: left;background-image: url(https://i.loli.net/2020/12/25/We1oCBFuTriEHvh.png);width: 11px;height: 11px;"></i>')
            $(".info .tags .time").eq(i).text(res[i]['pubdate']);
            $(".info .tags .time").eq(i).append(ii2);
            $(".up-name").eq(i).attr('href', 'javascript:;');
            $(".up-name").eq(i).text(res[i]['up_name']);
        }

        //隐藏其他video
        for (let i = res.length; i < 20; i++) {
            $(".img-anchor").eq(i).parent().css('display', 'none');
        }

        // 显示下面翻页按钮
        if (res.length === 0) {//一个都没有的时候，隐藏全部按钮
            $(".page-item").css('display', 'none');
        } else {
            // $(".page-item").eq(0).css("display", 'none'); // 隐藏上一页
            if (res[0]['page_num'] === 1) {
                for (let i = 0; i < $(".page-item").length; i++) {
                    $(".page-item").eq(i).css("display", 'none');
                }
            } else {// 不止一页的时候 只显示页数对应的btn
                for (let i = 1; i < res[0]['page_num'] + 1; i++) {
                    $(".page-item").eq(i).css("display", 'inline-block');
                }
                for (let i = res[0]['page_num'] + 1; i < $(".page-item").length - 1; i++) {
                    $(".page-item").eq(i).css("display", 'none');
                }
            }

        }

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