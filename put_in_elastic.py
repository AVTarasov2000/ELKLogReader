from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch()


def get_by_msg_id(msg_id):
    res = es.search(index="test_for_logreader_2", body={"query": {"match": {"MsgId":msg_id}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(message)s" % hit["_source"])


test_message = {
    'timestamp': datetime.now(),
    'message': "test2"
}

res = es.index(index="test-index", id=1, body=test_message)
print(res['result'])

# res = es.get(index="test_for_logreader_2", id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test_for_logreader_2", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(message)s" % hit["_source"])

# get_by_msg_id("X'414d512042524b303120202020202020609239712e4c7225'")















# curl -H'Content-Type: application/json' -XPUT "$ES_URL/blog/post/1?pretty" -d "{\"title\": \"Веселые котята\",\"content\": \"<p>Смешная история про котят<p>\",\"tags\": [\"котята\",\"смешная история\"],\"published_at\": \"2014-09-12T20:44:42+00:00\"}"