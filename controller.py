from flask import Flask, request, make_response
from flask_cors import CORS
from service import search_by_timestamp_and_msg_id, get_all_fields_to_search, search_by_args
from Node import Node

app = Flask(__name__)
CORS(app)

def make_resp(message, status):
    resp = make_response(message, status)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


@app.route("/")
def index():
    return "test"


@app.route("/search", methods=['POST'])
def test_get():
    data = request.json
    result = search_by_timestamp_and_msg_id(data['dateFrom'], data['dateTo'], data['msgId'])
    res = []
    if result['hits']['hits']:
        res = [{"message": str(i['_source']['message']).split("\n"), "timestamp": i['_source']['@timestamp']} for i in result['hits']['hits']]
    return {"result": res, "count": len(result['hits']['hits'])}


@app.route("/search/by/args", methods=['POST'])
def search():
    data = request.json
    result = search_by_args(data['queries'])
    res = []
    if result['hits']['hits']:
        res = [{"message": str(i['_source']['message']).split("\n"),
                "timestamp": i['_source']['@timestamp'],
                'path': i['_source']['path']}
               for i in result['hits']['hits']]
    return {"result": res, "count": len(result['hits']['hits'])}


@app.route("/getTree", methods=['GET'])
def get_tree():
    result, name = get_all_fields_to_search()
    root = Node(name, result, "", "")
    stack = []
    for i in result:
        if "properties" in result[i]:
            tmp = Node(i, result[i]["properties"], str(i), "")
            stack.append(tmp)
            root.items.append(tmp)
        else:
            root.items.append(Node(i, [], str(i), result[i]['type']))

    while stack:
        node = stack.pop()
        for n in node.content:
            if "properties" in node.content[n]:
                tmp = Node(n, node.content[n]["properties"], node.path+"."+n, node.content[n]['type'])
                stack.append(tmp)
                node.items.append(tmp)
            else:
                node.items.append(Node(n, [], node.path+"."+n, node.content[n]['type']))
    return root.get_json()




if __name__ == '__main__':
    app.run()