from flask import Flask, request
import uuid
import requests
import os
import random


os.environ['NO_PROXY'] = '127.0.0.1'
LOGGING_SERVICES = ["http://127.0.0.1:5002", "http://127.0.0.1:5003", "http://127.0.0.1:5004"]
MESSAGE_SERVICE = "http://127.0.0.1:5001"
app = Flask(__name__)


@app.route('/save', methods=["POST"])
def save():
    uid = str(uuid.uuid4())
    try:
        logging_service = LOGGING_SERVICES[random.randint(0, 2)]
        requests.post(logging_service + '/save', json={uid: request.json})
    except Exception as e:
        return f"Unable to save: {e}"
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    '''
    Retrieves data from logging and messages services as an concatenated string
    '''
    result_log = result_mes = None
    for service in LOGGING_SERVICES:
        try:
            result_log = requests.get(service + '/retrieve', json=request.json)
            result_mes = requests.get(MESSAGE_SERVICE + '/retrieve', json=request.json)
            break
        except Exception as e:
            print(f"Unable to get data from service: {e}")
    if result_log is None or result_mes is None:
        return ""
    return result_log.text + '|' + result_mes.text


if __name__ == '__main__':
    app.run()
