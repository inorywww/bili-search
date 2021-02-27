from elasticsearch import Elasticsearch


# for i in range(0, 220):
#     if es.indices.exists(index='index' + str(i)) is True:
#         es.indices.delete(index='index' + str(i), ignore=[400, 404])  # 删除index
# result = es.create(index='news', doc_type='politics', id=1, body=data)  # 添加数据
# result = es.update(index="news", doc_type='politics', body=data, id=1)  # 更新数据
# result = es.index(index='news', doc_type='politics', body=data, id=1)  # 更新数据
# result = es.delete(index='news', doc_type='politics', id=1)  # 删除数据

def query(f, keyword, size):
    es = Elasticsearch()

    data = {
        "from": f,
        "size": size,
        "query": {
            "multi_match": {
                "query": keyword,
                "type": "phrase_prefix",
                "fields": ["title", "bvid"],
            }
        },
        "highlight": {
            "pre_tags": "<em class='keyword'>",
            "post_tags": "</em>",
            "fields": {
                "title": {},
            }
        },
    }
    result = es.search(index="index*", doc_type="politics", body=data)  # 查询
    print(result)
    res = []
    for item in result['hits']['hits']:
        info = item['_source']
        if item.get('highlight') is not None:
            info['highlight'] = item['highlight']['title'][0]
        else:
            info['highlight'] = info['title']
        res.append(info)
    return res


def only_view_query(f, keyword, size, sortKeyword):
    es = Elasticsearch()
    data = {
        "from": f,
        "size": size,
        "query": {
            "multi_match": {
                "query": keyword,
                "type": "phrase_prefix",
                "fields": ["title", "bvid"],
            }
        },
        "highlight": {
            "pre_tags": "<em class='keyword'>",
            "post_tags": "</em>",
            "fields": {
                "title": {},
                "bvid": {}
            }
        },
        "sort": {
            sortKeyword: {
                "order": "desc"
            }
        }
    }

    result = es.search(index="index*", doc_type="politics", body=data)  # 查询
    res = []
    for item in result['hits']['hits']:
        info = item['_source']
        info['highlight'] = item['highlight']['title'][0]
        res.append(info)
    return res


def only_filter_query(f, keyword, size, start_time, end_time):
    es = Elasticsearch()
    data = {
        "from": f,
        "size": size,

        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": keyword,
                        "type": "phrase_prefix",
                        "fields": ["title", "bvid"],
                    }
                },
                "filter": {
                    "range": {
                        'duration': {
                            "gte": int(start_time * 60),
                            "lte": int(end_time * 60)
                        }
                    }
                }
            }
        },
        "highlight": {
            "pre_tags": "<em class='keyword'>",
            "post_tags": "</em>",
            "fields": {
                "title": {},
                "bvid": {}
            }
        },
    }
    result = es.search(index="index*", doc_type="politics", body=data)  # 查询
    res = []
    for item in result['hits']['hits']:
        info = item['_source']
        # print(item['highlight']['title'][0])
        info['highlight'] = item['highlight']['title'][0]
        res.append(info)
    return res


def view_and_filter_query(f, keyword, size, view_way, start_time, end_time):
    es = Elasticsearch()
    data = {
        "from": f,
        "size": size,

        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": keyword,
                        "type": "phrase_prefix",
                        "fields": ["title", "bvid"],
                    }
                },
                "filter": {
                    "range": {
                        'duration': {
                            "gte": int(start_time * 60),
                            "lte": int(end_time * 60)
                        }
                    }
                }
            }
        },

        "highlight": {
            "pre_tags": "<em class='keyword'>",
            "post_tags": "</em>",
            "fields": {
                "title": {},
                "bvid": {}
            }
        },
        "sort": {
            view_way: {
                "order": "desc"
            }
        },

    }
    result = es.search(index="index*", doc_type="politics", body=data)  # 查询
    res = []
    for item in result['hits']['hits']:
        info = item['_source']
        # print(item['highlight']['title'][0])
        info['highlight'] = item['highlight']['title'][0]
        res.append(info)
    return res


if __name__ == '__main__':
    res = query(0, "华为", 10)
    # res = query(0, "明日方舟", 10)
    # res = sort_query(5, "明日方舟", 10,'pubdate')
    # res = filter_query(5, "明日方舟", 10, 'pubdate', "duration", 10, 30)
    # res = only_filter_query(0, "明日方舟", 200, 10, 30)
    # res = view_and_filter_query(0, "明日方舟", 200, 'pubdate', 10, 30)
    for i in res:
        print(i)
    print(len(res))
