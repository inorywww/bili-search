import requests

# 获取用户mid
def get_mid(bvid):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
    }
    url = "http://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    document = requests.get(url, headers=header)
    data = document.json()
    return data['data']['owner']['mid']


if __name__ == '__main__':
    bvid = 'BV1BZ4y1G7od'
    get_mid(bvid)
