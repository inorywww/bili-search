import requests
from elasticsearch import Elasticsearch


def saveES(index_name, data):
    es = Elasticsearch()
    # 如果没有该索引就先创建
    index_name = 'index' + str(index_name)
    if es.indices.exists(index=index_name) is not True:
        es.indices.create(index=index_name, ignore=400)  # 创建索引
    es.index(index=index_name, doc_type='politics', body=data)  # 添加数据


def get_info(item):
    if item is None:
        return

    bvid = item['bvid']  # bv号
    tid = item['tid']  # 分区号
    picSrc = item['pic']  # 封面链接
    title = item['title']  # 视频标题
    duration = item['duration']  # 视频持续时间
    pubdate = item['pubdate']  # 视频发布时间
    up_name = item['owner']['name']  # up名字
    view = item['stat']['view']  # 播放量
    info = {
        "bvid": bvid,
        "tid": tid,
        "pic": picSrc,
        "title": title,
        "duration": duration,
        "pubdate": pubdate,
        "up_name": up_name,
        "view": view
    }
    return info
    # info.append(info)


if __name__ == '__main__':
    header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0",
              "Cookie": ""}
    tunnel = "tps114.kdlapi.com:15818"
    proxies = {
        "http": "http://%(proxy)s/" % {"proxy": tunnel},
        "https": "http://%(proxy)s/" % {"proxy": tunnel}
    }
    f = open("links.txt")
    lines = f.readlines()
    f.close()
    infos = []
    j = 0
    for line in lines:
        print(j)
        # print(line)
        url = "https://api.bilibili.com/x/web-interface/view?bvid=" + line
        try:
            document = requests.get(url, headers=header, proxies=proxies)
            item = document.json()
            for data in item['data']:
                infos.append(get_info(data))
                # saveES("index" + str(j['tid']), data)
        except Exception as e:
            print("error")
            pass
        j += 1
    print(lines)
    for info in infos:
        saveES("index" + str(j['tid']), info)

# saveES("index", {})
