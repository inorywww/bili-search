import os
import random
import re  # 正则，文字匹配
import threading
import time
from bs4 import BeautifulSoup
import requests
from collections import Counter
from elasticsearch import Elasticsearch
from save_to_ES import saveES


class bvQueue:
    def __init__(self):
        self.visited = []  # 已访问的url
        self.unVisited = []  # 未访问的url

    # 获取访问过的url队列
    def getVisitedUrl(self):
        return self.visited

    # 获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited

    # url添加到访问过的队列中
    def addVisitedUrl(self, url):
        self.visited.append(url)

    # 移除访问过的url
    def removeVisitedUrl(self, url):
        self.visited.remove(url)

    # 取出未访问过的url
    def unVisitedUrlDeQueue(self):
        try:
            return self.unVisited.pop()
        except:
            return None

    # 保证每个url只被访问一次
    def addUnvisitedUrl(self, url):
        if url != "" and url not in self.visited and url not in self.unVisited:
            self.unVisited.insert(0, url)

    # 判断未访问的url队列是否为空
    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited) == 0


class spider_bili:
    def __init__(self):
        self.original_url = "https://api.bilibili.com/x/web-interface/"
        self.popular_bvs = []  # 存放热门的视频
        self.recent_bvs = []  # 存放最新的视频
        self.original_bvs = []  # 存放种子站点
        self.info = []  # 存放所有视频信息
        self.bvs = []  # 存放所有bv号
        self.tids = []
        self.depth = 20
        self.nowDepth = 1
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
            'Referer': 'https://api.bilibili.com'
        }

        # ip池
        self.tunnel = "tps114.kdlapi.com:15818"
        self.proxies = {
            "http": "http://%(proxy)s/" % {"proxy": self.tunnel},
            "https": "http://%(proxy)s/" % {"proxy": self.tunnel}
        }

    def spider(self):
        tid = 200
        # 获取种子节点
        self.get_recent(tid)
        self.get_popular(tid)
        print(self.original_bvs)
        # return
        temps = []
        for original_bv in self.original_bvs:
            if len(original_bv) != 0:
                temps.append(original_bv)
        temps1 = temps[0:int(len(temps) / 2)]
        temps2 = temps[int(len(temps) / 2):len(temps)]

        # 多线程爬取
        threadlist = []
        for original_bv in temps1:
            if len(original_bv) != 0:
                t = threading.Thread(target=self.get_all_links, args=(original_bv,))
                t.start()
                threadlist.append(t)
        for thd in threadlist:
            thd.join()

        for original_bv in temps2:
            if len(original_bv) != 0:
                t = threading.Thread(target=self.get_all_links, args=(original_bv,))
                t.start()
                threadlist.append(t)
        for thd in threadlist:
            thd.join()

        for i in self.info:
            if i is None:
                self.info.remove(i)
                continue
            # print(i['bvid'])
            self.saveUrl(i['bvid'])
        print("总爬取数量为：" + str(len(self.info)))
        # 查找是否有重复元素
        # b = dict(Counter(a))
        # print("重复元素：")
        # print({key: value for key, value in b.items() if value > 1})  # 展现重复元素和重复次数

        # 保存到数据库
        print("保存到DB中...")
        self.saveES()

    def testTid(self, tid):
        t2 = []
        for i in range(0, tid):
            print("tid=" + str(i))
            self.tids.append(i)
            try:
                url = "https://api.bilibili.com/x/web-interface/dynamic/region?rid=" + str(i) + "&ps=1&pn=1"
                document = requests.get(url, headers=self.header, proxies=self.proxies)
                print(document.json())
            except Exception as e:
                t2.append(i)
                print("已失效")
                print(i)
                pass
        for t in t2:
            if t in self.tids:
                self.tids.remove(t)
        print(self.tids)
        print("有效的tid长度：" + str(len(self.tids)))

    # 获取分区最新视频
    def get_recent(self, tid):
        # https://api.bilibili.com/x/web-interface/dynamic/region?rid=22&ps=1&pn=1
        original_url = self.original_url + "dynamic/region?rid="
        ps = "50"
        pn = "1"
        expiredTid = []
        j = 0
        for i in range(tid):
            time.sleep(0.5)
            self.recent_bvs.append([])
            try:
                print("tid=" + str(i))
                url = original_url + str(i) + "&ps=" + ps + "&pn=" + pn
                document = requests.get(url, headers=self.header)
                datas = document.json()
                for data in datas['data']['archives']:
                    if data['bvid'] not in self.bvs:
                        self.recent_bvs[j].append(data['bvid'])
                        self.bvs.append(data['bvid'])
                        self.info.append(self.get_info(data))
            except Exception as e:
                print('失败')
                expiredTid.append(i)
            self.original_bvs.append(self.recent_bvs[j])
            j += 1
            print("---------------")
            continue
        print("失败的tid：")
        print(expiredTid)
        print(len(expiredTid))

    # 获取指定分区热门前十一视频
    def get_popular(self, tid):
        original_url = self.original_url + "ranking/region?rid="
        day = "3"
        j = 0
        expiredTid = []

        for i in range(0, tid):
            time.sleep(0.5)
            self.popular_bvs.append([])
            try:
                print("tid=" + str(i))
                url = original_url + str(i) + "&day=" + day
                document = requests.get(url, headers=self.header, timeout=(5, 5))
                datas = document.json()
                for data in datas['data']:
                    # if data['bvid'] not in self.bvs:
                    #     self.bvs.append(data['bvid'])
                    #     print(data)
                    #     self.get_info(data)
                    #     print('----')
                    self.popular_bvs[j].append(data['bvid'])
            except Exception as e:
                print('失败')
                expiredTid.append(i)
            self.original_bvs[j] += self.popular_bvs[j]
            j += 1
            print("---------------")
            continue
        print("失败的tid：")
        print(expiredTid)
        print(len(expiredTid))

    # 爬取推荐视频
    def get_recommend(self, bvid):
        links = []
        if bvid == "":
            print("空bvid")
            return links
        original_url = self.original_url + "archive/related?bvid=" + bvid
        f = 0
        while f < 3:
            try:
                document = requests.get(original_url, headers=self.header, timeout=(2, 2), proxies=self.proxies)
                item = document.json()
                for i in item['data']:
                    links.append(i['bvid'])
                    if i['bvid'] not in self.bvs:
                        self.bvs.append(i['bvid'])
                        self.get_info(i)
                return links
            except Exception as e:
                time.sleep(1)
                print(f)
                print("error")
                f += 1

        return links

    # 根据指定的初始bv爬取
    def get_all_links(self, original_bv):
        queue = bvQueue()
        for i in original_bv:
            queue.addUnvisitedUrl(i)
        links = []
        while self.nowDepth < self.depth:
            # 未抓取的链接不为空的时候
            while not queue.unVisitedUrlsEnmpy():
                # 将对头出列
                url = queue.unVisitedUrlDeQueue()
                if url is None or url == "":
                    print("url is none")
                    continue
                # 获取超链接
                links = self.get_recommend(url)
                time.sleep(0.2)
                print("links:")
                print(links)
                print('-------------------------')
                # for link in links:
                #     self.saveUrl(link)
                # 将url放入已访问的url中
                queue.addVisitedUrl(url)
            # 未访问的url入列
            for link in links:
                queue.addUnvisitedUrl(link)
            self.nowDepth += 1

    # 获取视频信息
    def get_info(self, item):
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

        self.info.append(info)

    def get_info_(self, bvid):
        url = self.original_url + "/view?bvid=" + bvid
        try:
            document = requests.get(url, headers=self.header, proxies=self.proxies)
            item = document.json()
            bvid = item['data']['bvid']  # bv号
            tid = item['data']['tid']  # 分区号
            picSrc = item['data']['pic']  # 封面链接
            title = item['data']['title']  # 视频标题
            duration = item['data']['duration']  # 视频持续时间
            pubdate = item['data']['pubdate']  # 视频发布时间
            up_name = item['data']['owner']['name']  # up名字
            view = item['data']['stat']['view']  # 播放量
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
            self.info.append(info)
        except Exception as e:
            print("error")

    def saveUrl(self, url):
        with open("D:\OneDrive\python\SearchEngine\课程设计\SE\links.txt", mode="a", encoding="utf-8") as f:
            f.write(url)
            f.write('\n')
            f.close()

    # 保存到es
    def saveES(self):
        for info in self.info:
            saveES(info['tid'], info)


if __name__ == '__main__':
    spider = spider_bili()
    spider.spider()
