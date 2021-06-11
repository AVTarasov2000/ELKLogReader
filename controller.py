from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "test"

@app.route("/test")
def test_get():
    return {
        'timestamp': "20.09.11 20:20:20.299330",
        'message':"test"
            }

if __name__ == '__main__':
    app.run()