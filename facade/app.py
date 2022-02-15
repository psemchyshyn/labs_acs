from flask import Flask, request, jsonify
import requests
import os


os.environ['NO_PROXY'] = '127.0.0.1'
STORAGE = "http://127.0.0.1:5001"
STATIC = "http://127.0.0.1:5002"
app = Flask(__name__)


@app.route('/save', methods=["POST"])
def save():
    try:
        requests.post(STORAGE + '/save', json=request.json)
    except Exception as e:
        return f"Unable to save: {e}"
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    '''
    Accepts json body as a dict {"keys": []}, whose values we want to retrieve
    :return: [] - list of values
    '''
    result = None
    try:
        result = requests.get(STORAGE + '/retrieve', json=request.json)
    except Exception as e:
        return f"Unable to get data from the storage: {e}"
    return jsonify(result.json()), result.status_code


@app.route('/', methods=["GET", "POST"])
def do_something():
    if request.method == "GET":
        return requests.get(STATIC + '/', json=request.json).content
    else:
        requests.post(STATIC + '/', json=request.json)
        return f"Posted successfully"

if __name__ == '__main__':
    app.run()
