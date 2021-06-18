from elasticsearch import Elasticsearch
es = Elasticsearch()
es_info = Elasticsearch.info(es)

index = "test_for_logreader"


def search_by_msg_id(msg_id: str):
    return es.search(index=index, body={"query": {"match": {"MsgId": msg_id}}})


def search_by_timestamp(start_date: str, end_date: str):
    return es.search(index=index, body={"query": {"range": {"timestamp": {"gte": start_date, "lte": end_date}}}})


def search_by_timestamp_and_msg_id(start_date: str, end_date:str, msg_id:str):
    if not msg_id:
        msg_id = "*"
    if not end_date:
        end_date = "*"
    if not start_date:
        start_date = "*"
    return es.search(index=index, body={"size":1000 ,"query": {"query_string": {
    "query": f"@timestamp:[{start_date} TO {end_date}] AND MsgId:\"{msg_id}\""}}})


def get_all_fields_to_search():
    return es.indices.get_mapping(index=index)['test_for_logreader']['mappings']['properties'], index


def search_by_args(queries):
    if len(queries) <= 0:
        return es.search(index=index, body={"size":1000 ,"query": {"match_all" :{}}})
    else:
        query = queries[0]
        for q in queries[1:]:
            query += f"AND {q}"
        return es.search(index=index, body={"size":1000 ,"query": {"query_string": {
                "query": query}}})


# print(es.indices.get_mapping(index="test_for_logreader"))

# print(es.search(index="test-index", sort={"timestamp": "desc"}))

# print(es.search(index="test-index", body={"query":{"constant_score":{"filter": {"range":{"timestamp": {"lt": "2014-09-01"}}}}}}))

# print(es.search(index="test-index", body={"query": {"range": {"timestamp": {"gte": "2014-09-01", "lte": "2022-09-01"}}, "match": {"message": "test1"}}}))


# print(len(es.search(index="test_for_logreader", body={"query": {"query_string": {
#     "query":"@timestamp:[* TO *] AND   params.APPLICANTTYPE:'должник'"}}})['hits']['hits']))

print(es.search(index=index, body={"query": {"match_all": {}}})['hits']['hits'])

# for i in es.indices.get_mapping(index=index)['test_for_logreader']['mappings']['properties']:
#     print(i)
# print()
# for i in es.indices.get_mapping(index=index)['test_for_logreader']['mappings']['properties']['params']['properties']:
#     print(i)