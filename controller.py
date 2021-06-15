from flask import Flask, request, make_response
from flask_cors import CORS
from service import search_by_timestamp_and_msg_id, get_all_fields_to_search
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

@app.route("/getTree", methods=['POST'])
def get_tree():
    result = get_all_fields_to_search()
    node = Node("nodes", result)
    for n in node.content:
        if node.content[n].contains("properties"):
            pass



if __name__ == '__main__':
    app.run()