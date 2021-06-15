from flask import Flask, request, make_response
from flask_cors import CORS
from service import search_by_timestamp_and_msg_id

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
        res = [{"message": i['_source']['message'], "timestamp": i['_source']['@timestamp']} for i in result['hits']['hits']]
    return {"result": res, "count": len(result['hits']['hits'])}

if __name__ == '__main__':
    app.run()