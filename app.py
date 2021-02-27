import json
import os
import queue
import time

from flask import Flask, render_template, request, redirect, url_for, session

import seDB.query_bili as qb
import seDB.spider_hotlist as sh
import seDB.spider_mid as sm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def get_hotlist():
    hotlist = sh.get_hot()
    return hotlist


def get_mid(bvid):
    mid = sm.get_mid(bvid)
    return "https://space.bilibili.com/" + str(mid)


@app.route('/clear_history', methods=['GET', 'POST'])
def clear_history():
    f = open('history.txt', 'w')
    f.close()
    return json.dumps({})


@app.route('/history', methods=['GET', 'POST'])
def his():
    data1 = request.get_json()
    f = open('history.txt', 'r')
    lines = f.readlines()
    f.close()
    histories = []
    for line in lines:
        res1 = {'his': line.split("\n")[0]}
        histories.append(res1)
    return json.dumps(histories)


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    data1 = request.get_json()
    res1 = qb.query(0, data1['keyword'], 10)
    return json.dumps(res1)


# 播放量和发布时间排序
@app.route('/view', methods=['GET', 'POST'])
def filter_view():
    global res
    info = []
    data1 = request.get_json()
    if data1['way'] == '':
        res = qb.query(0, data1['keyword'], 200)
    else:
        res = qb.only_view_query(0, data1['keyword'], 200, data1['way'])
    res1 = res[:20]
    for d in res1:
        d['duration'] = duration_change(d['duration'])
        d['pubdate'] = str(time.gmtime(d['pubdate']).tm_year) + "-" + str(time.gmtime(d['pubdate']).tm_mon) + "-" + str(
            time.gmtime(d['pubdate']).tm_mday)
        d['view'] = view_change(d['view'])
        d['href'] = "https://www.bilibili.com/video/" + d['bvid']
        info.append(d)
    print("info:")
    print(info)
    print(len(info))
    return json.dumps(info)


@app.route('/view_time', methods=['GET', 'POST'])
def filter_time():
    global res
    info = []
    data1 = request.get_json()
    print(data1)
    if data1['view_way'] == '':
        if data1['start_time'] == 0 and data1['end_time'] == 0:
            res = qb.query(0, data1['keyword'], 200)
        else:
            res = qb.only_filter_query(0, data1['keyword'], 200, data1['start_time'], data1['end_time'])
    else:
        if data1['start_time'] == 0 and data1['end_time'] == 0:
            res = qb.only_view_query(0, data1['keyword'], 200, data1['view_way'])
        else:
            res = qb.view_and_filter_query(0, data1['keyword'], 200, data1['view_way'], data1['start_time'],
                                           data1['end_time'])

    res1 = res[:20]
    print(len(res))
    nums = turn_page()
    page_num = nums[-1]
    print("page_num")
    print(page_num)
    for d in res1:
        d['duration'] = duration_change(d['duration'])
        d['pubdate'] = str(time.gmtime(d['pubdate']).tm_year) + "-" + str(time.gmtime(d['pubdate']).tm_mon) + "-" + str(
            time.gmtime(d['pubdate']).tm_mday)
        d['view'] = view_change(d['view'])
        d['href'] = "https://www.bilibili.com/video/" + d['bvid']
        d['page_num'] = page_num
        info.append(d)
    print("info:")
    print(info)
    return json.dumps(info)

    pass


@app.route('/', methods=['GET'])
def hello_world():
    global flag

    histories = read_history()
    flag = 0
    hotlist = get_hotlist()
    hotlist_1_3 = []
    hotlist_4_10 = []
    hotlist_11_20 = []
    for i in range(0, 3):
        hotlist_1_3.append(hotlist[i])
    for i in range(3, 10):
        hotlist_4_10.append(hotlist[i])
    for i in range(10, 20):
        hotlist_11_20.append(hotlist[i])
    return render_template('search_bili.html', hotlist_1_3=hotlist_1_3, hotlist_4_10=hotlist_4_10,
                           hotlist_11_20=hotlist_11_20, historys=histories)


data = {}


@app.route('/query', methods=['POST', 'GET'])  # 路由
def get_keyword():
    global data
    global flag
    flag = 0
    data = request.get_json()
    save_history(data['keyword'])
    print("1:")
    print(data)
    s = {'bvid': 'BV1DA411s7RU',
         'tid': 138,
         'pic': 'http://i2.hdslb.com/bfs/archive/469a3d8bb80ea8644aba7224aa394ff5decd751a.jpg',
         'title': '圣 诞 劫',
         'duration': 187,
         'pubdate': 1608690288,
         'up_name': '有辱斯文嗷',
         'view': 65246
         }
    return json.dumps(data)


page_flag = 0
res = []


@app.route('/search/', methods=['POST', 'GET'])
def search():
    global data
    global page_flag
    global res
    info = []

    res = qb.query(0, data['keyword'], 200)
    print("2:")
    print(data)
    nums = turn_page()
    res1 = res[:20]
    for d in res1:
        d['duration'] = duration_change(d['duration'])
        d['pubdate'] = str(time.gmtime(d['pubdate']).tm_year) + "-" + str(time.gmtime(d['pubdate']).tm_mon) + "-" + str(
            time.gmtime(d['pubdate']).tm_mday)
        d['view'] = view_change(d['view'])
        d['href'] = "https://www.bilibili.com/video/" + d['bvid']
        # d['mid'] = get_mid(d['bvid'])
        info.append(d)
    print("info:")
    print(info)
    print(len(info))

    return render_template('search_result.html', keyword=data['keyword'], video_infos=info,
                           nums=nums)


@app.route('/page', methods=['POST', 'GET'])
def pages():
    global res
    data1 = request.get_json()
    page_num = int(data1['page_num'])
    print("page_num")
    print(page_num)
    res1 = res[page_num * 20:page_num * 20 + 20]
    info = []
    for d in res1:
        d['duration'] = duration_change(d['duration'])
        d['pubdate'] = pubdate_change(d['pubdate'])
        d['view'] = view_change(d['view'])
        d['href'] = "https://www.bilibili.com/video/" + d['bvid']
        info.append(d)
    print(info)
    return json.dumps(info)


def read_history():
    f = open('history.txt', 'r')
    lines = f.readlines()
    f.close()
    histories = []
    for line in lines:
        histories.append(line.split("\n")[0])
    return histories


def save_history(keyword):
    f = open('history.txt', 'r')
    lines = f.readlines()
    f.close()
    histories = []
    for line in lines:
        histories.append(line.split("\n")[0])

    if keyword not in histories:
        if len(histories) >= 10:
            del histories[0]
        histories.append(keyword)
    f1 = open('history.txt', 'w+')
    for i in histories:
        f1.write(i)
        f1.write('\n')
    f1.close()
    histories.reverse()
    return histories


# 翻页功能
def turn_page():
    global page_flag
    global res
    page_len = int((len(res) / 20)) + 1
    nums = []
    if len(res) % 20 == 0:
        page_len -= 1
    for i in range(1, page_len + 1):
        nums.append(i)
    return nums


@app.route('/search/?keyword=<keyword>', methods=['POST', 'GET'])
def search_keyword(keyword):
    print(keyword)
    return keyword


def view_change(view):
    if isinstance(view, str):
        return view
    if view < 10000:
        return str(view)
    elif view >= 10000:
        res1 = view / 10000
        return ('%.1f' % res1) + '万'


def duration_change(duration):
    if isinstance(duration, str):
        return duration
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    if int(h) == 0:
        return "%02d:%02d" % (m, s)
    return "%d:%02d:%02d" % (h, m, s)


def pubdate_change(pubdate):
    if isinstance(pubdate, str):
        return pubdate
    return str(time.gmtime(pubdate).tm_year) + "-" + str(time.gmtime(pubdate).tm_mon) + "-" + str(
        time.gmtime(pubdate).tm_mday)


if __name__ == '__main__':
    app.run()
