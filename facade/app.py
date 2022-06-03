"""This module must be run the last one."""
from flask import Flask, request
import uuid
import hazelcast
import requests
import os
import random
import consul
import sys

os.environ['NO_PROXY'] = '127.0.0.1'

port = int(sys.argv[1])
LOGGING_SERVICES = []
MESSAGE_SERVICES = []
app = Flask(__name__)

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('facade-service', port=port, service_id=f"facade_{str(uuid.uuid4())}")

services = session.agent.services()

for key, value in services.items():
    service_type = key[0]
    if service_type == "l":
        LOGGING_SERVICES.append(f"http://localhost:{value['Port']}/")
    elif service_type == "m":
        MESSAGE_SERVICES.append(f"http://localhost:{value['Port']}/")

print(LOGGING_SERVICES)
client = hazelcast.HazelcastClient()
q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()


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
    app.run(port=port)
