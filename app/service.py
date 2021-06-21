import datetime

from elasticsearch import Elasticsearch
es = Elasticsearch()
es_info = Elasticsearch.info(es)

index = "test_for_logreader_2"


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
    return es.indices.get_mapping(index=index)[index]['mappings']['properties'], index


def search_by_args(queries):
    if len(queries) <= 0:
        return es.search(index=index, body={"size":1000 ,"query": {"match_all" :{}}})
    else:
        query = queries[0]
        for q in queries[1:]:
            query += f"AND {q}"
        return es.search(index=index, body={"size":1000 ,"query": {"query_string": {
                "query": query}}})


def difference_by_id():
    with open("res", "w") as f:
        for id in es.search(index=index, body={"size": 10000,  "fields": ["params.HTTPRequestId"], "_source": False})['hits']['hits']:
            message = ""
            var = es.search(index=index,
                            body={"query": {"match": {
                                "params.HTTPRequestId": f"{id['fields']['params.HTTPRequestId']}"
                            }}
                            ,"fields": ['log_timestamp'], "_source": False})['hits']['hits']

            if len(var) > 2:
                message += str(id['fields']['params.HTTPRequestId'][0])+"\n"
                message+= f"{var[0]['fields']['log_timestamp'][0]} - {var[1]['fields']['log_timestamp'][0]} = "
                message += str((datetime.datetime.strptime(var[0]['fields']['log_timestamp'][0], "%Y-%m-%d %H:%M:%S.%f")
                               - datetime.datetime.strptime(var[1]['fields']['log_timestamp'][0], "%Y-%m-%d %H:%M:%S.%f")).microseconds)
                message+="\n\n"
            f.write(message)

# difference_by_id()
# print(es.search(index=index, body={"query": {"match": {"params.RequestId": "X'50400000000000022fc75e9ebe5611eb850bac100e1f0000'"}}}))

# print(es.search(index=index, body={"size": 10000,  "fields": ["params.HTTPRequestId"], "_source": False})['hits']['hits'])

# print(es.search(index=index, body={"size": 1000,  "fields": ["params.HTTPRequestId"], "_source": False})['hits']['hits'])
# print(es.indices.get_mapping(index="test_for_logreader"))

# print(es.search(index="test-index", sort={"timestamp": "desc"}))

# print(es.search(index="test-index", body={"query":{"constant_score":{"filter": {"range":{"timestamp": {"lt": "2014-09-01"}}}}}}))

# print(es.search(index="test-index", body={"query": {"range": {"timestamp": {"gte": "2014-09-01", "lte": "2022-09-01"}}, "match": {"message": "test1"}}}))


# print(es.search(index=index, body={"query": {"query_string": {
#     "query":"params.RequestId: \"X'5040000000000002dbc4b01ec47a11ebb6baac100e1f0000'\""}}})['hits']['hits'])
#
# print(es.search(index=index, body={"query": {"match_all": {}}})['hits']['hits'])

# for i in es.indices.get_mapping(index=index)['test_for_logreader']['mappings']['properties']:
#     print(i)
# print()
# for i in es.indices.get_mapping(index=index)['test_for_logreader']['mappings']['properties']['params']['properties']:
#     print(i)