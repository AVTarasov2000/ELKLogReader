from elasticsearch import Elasticsearch
es = Elasticsearch()
es_info = Elasticsearch.info(es)


def search_by_msg_id(msg_id: str):
    return es.search(index="test-index", body={"query": {"match": {"MsgId": msg_id}}})


def search_by_timestamp(start_date: str, end_date:str):
    return es.search(index="test-index", body={"query": {"range": {"timestamp": {"gte": start_date, "lte": end_date}}}})


def search_by_timestamp_and_msg_id(start_date: str, end_date:str, msg_id:str):
    if not msg_id:
        msg_id = "*"
    if not end_date:
        end_date = "*"
    if not start_date:
        start_date = "*"
    return es.search(index="test-index", body={"query": {"query_string": {
    "query": f"timestamp:[{start_date} TO {end_date}] AND MsgId:\"{msg_id}\""}}})

# print(es.indices.get_mapping(index="test-index"))

# print(es.search(index="test-index", sort={"timestamp": "desc"}))

# print(es.search(index="test-index", body={"query":{"constant_score":{"filter": {"range":{"timestamp": {"lt": "2014-09-01"}}}}}}))

# print(es.search(index="test-index", body={"query": {"range": {"timestamp": {"gte": "2014-09-01", "lte": "2022-09-01"}}, "match": {"message": "test1"}}}))


# print(es.search(index="test-index", body={"query": {"query_string": {
#     "query":"timestamp:[* TO *] AND message:\"*\""}}}))