import datetime
import os
from elasticsearch import Elasticsearch
# es = Elasticsearch("http://localhost:9200")
es = Elasticsearch("http://elasticsearch:9200")


index = "logreader"


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
    return es.search(index=index, body={"size":10000 ,"query": {"query_string": {
    "query": f"@timestamp:[{start_date} TO {end_date}] AND MsgId:\"{msg_id}\""}}})


def get_all_fields_to_search():
    es.indices.create(index=index, ignore=400)
    res = es.indices.get_mapping(index=index)[index]['mappings']
    if 'properties' in res:
        return res['properties'], index
    else:
        return [], index


def search_by_args(queries):
    if len(queries) <= 0:
        return es.search(index=index, body={"size":10000 ,"query": {"match_all" :{}}})
    else:
        query = queries[0]
        for q in queries[1:]:
            query += f"AND {q}"
        return es.search(index=index, body={"size":10000 ,"query": {"query_string": {
                "query": query}}})


def difference_by_id(file1, file2, field_path):
    res = []
    for id in es.search(index=index, body={"size": 10000,  "fields": [field_path], "_source": False})['hits']['hits']:
        message = []
        var1 = es.search(index=index,body = {"size": 1000,
                                             "query": {
                                                 "query_string": {
                                                    "query": f"{field_path}: \"{id['fields'][field_path][0]}\" AND path: \"{file1}\""
                                                 }
                                             }
                                            ,"fields": ['log_timestamp'], "_source": False})['hits']['hits']
        var2 = es.search(index=index,body = {"size": 1000,
                                             "query": {
                                                 "query_string": {
                                                    "query": f"{field_path}: \"{id['fields'][field_path][0]}\" AND path: \"{file2}\""
                                                 }
                                             }
                                            ,"fields": ['log_timestamp'], "_source": False})['hits']['hits']
        if var1 and var2:
            message.append(str(id['fields'][field_path][0]))
            message.append(f"{var1[0]['fields']['log_timestamp'][0]} - {var2[0]['fields']['log_timestamp'][0]} = " +
                           str((datetime.datetime.strptime(var1[0]['fields']['log_timestamp'][0], "%Y-%m-%d %H:%M:%S.%f")
                           - datetime.datetime.strptime(var2[0]['fields']['log_timestamp'][0], "%Y-%m-%d %H:%M:%S.%f")).microseconds))
        res.append({"message":message, "path": f"{file1} - {file2}"})
    return res


def delete_index():
    es.indices.delete(index=index, ignore=[400, 404])
    es.indices.create(index=index, ignore=400)

# difference_by_id()
# print(es.search(index=index, body={"query": {"match": {"params.RequestId": "X'50400000000000022fc75e9ebe5611eb850bac100e1f0000'"}}}))

# print(es.search(index=index, body={"size": 10000,  "fields": ["@timestamp"], "_source": False})['hits']['hits'])

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