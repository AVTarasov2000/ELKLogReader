# from waitress import serve
from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from app.service import search_by_timestamp_and_msg_id, get_all_fields_to_search, search_by_args, difference_by_id, delete_index
from app.Node import Node

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/search/difference", methods=['POST'])
def difference():
    data = request.json
    res = difference_by_id(data['file1'], data['file2'], data['field'])
    return {"result": res, "count": len(res)}


@app.route("/index/delete", methods=['GET'])
def del_index():
    delete_index()
    return {}


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
