from flask import Flask, request
import uuid
import hazelcast
import requests
import os
import random


os.environ['NO_PROXY'] = '127.0.0.1'
LOGGING_SERVICES = ["http://127.0.0.1:5003", "http://127.0.0.1:5004", "http://127.0.0.1:5005"]
MESSAGE_SERVICES = ["http://127.0.0.1:5001", "http://127.0.0.1:5001"]
app = Flask(__name__)

client = hazelcast.HazelcastClient()
q = client.get_queue("message-queue")


@app.route('/save', methods=["POST"])
def save():
    uid = str(uuid.uuid4())
    try:
        logging_service = LOGGING_SERVICES[random.randint(0, 2)]
        q.put(request.json).result()
        requests.post(logging_service + '/save', json={uid: request.json})
    except Exception as e:
        return f"Unable to save: {e}"
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    '''
    Retrieves data from logging and messages services as an concatenated string
    '''
    result_log = result_mes = ""
    random.shuffle(LOGGING_SERVICES)
    random.shuffle(MESSAGE_SERVICES)

    for log_service in LOGGING_SERVICES:
        try:
            result_log = requests.get(log_service + '/retrieve', json=request.json).text
            break
        except Exception as e:
            print(f"Unable to get data from logging service: {e}")

    for mes_service in MESSAGE_SERVICES:
        try:
            result_mes = requests.get(mes_service + '/retrieve', json=request.json).text
            break
        except Exception as e:
            print(f"Unable to get data from message service: {e}")

    return result_log + '|' + result_mes


if __name__ == '__main__':
    app.run()
