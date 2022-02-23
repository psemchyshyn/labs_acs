from flask import Flask, request
import uuid
import requests
import os


os.environ['NO_PROXY'] = '127.0.0.1'
LOGGING_SERVICE = "http://127.0.0.1:5001"
MESSAGE_SERVICE = "http://127.0.0.1:5002"
app = Flask(__name__)


@app.route('/save', methods=["POST"])
def save():
    uid = str(uuid.uuid4())
    try:
        requests.post(LOGGING_SERVICE + '/save', json={uid: request.json})
    except Exception as e:
        return f"Unable to save: {e}"
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    '''
    Retrieves data from logging and messages services as an concatenated string
    '''
    try:
        result_log = requests.get(LOGGING_SERVICE + '/retrieve', json=request.json)
        result_mes = requests.get(MESSAGE_SERVICE + '/retrieve', json=request.json)
    except Exception as e:
        return f"Unable to get data from servies: {e}"
    return result_log.text + '|' + result_mes.text


if __name__ == '__main__':
    app.run()
