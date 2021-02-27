import requests


# 热搜列表
def get_hot():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
    }
    url = 'http://s.search.bilibili.com/main/hotword'
    document = requests.get(url, headers=header)
    data = document.json()
    res = []
    for i in data['list']:
        info = {
            'id': i['id'],
            'keyword': i['keyword'],
        }
        res.append(info)
    print(len(res))
    return res


if __name__ == '__main__':
    get_hot()
