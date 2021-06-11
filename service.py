from elasticsearch import Elasticsearch
es = Elasticsearch()
es_info = Elasticsearch.info(es)


def search_by_msg_id(msg_id: str):
    es.search(index="test-index", body={"query": {"match": {"MsgId": msg_id}}})


def search_by_timestamp(start_date: str, end_date:str):
    print(es.search(index="test-index", body={"query":{"constant_score":{"filter": {"range":[{"timestamp": {"gte": start_date}}, {"lt": end_date}]}}}}))


# print(es.indices.get_mapping(index="test-index"))

# print(es.search(index="test-index", sort={"timestamp": "desc"}))

print(es.search(index="test-index", body={"query":{"constant_score":{"filter": {"range":{"timestamp": {"lte": "2014-09-01"}}}}}}))