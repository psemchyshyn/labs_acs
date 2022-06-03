import hazelcast
from flask import Flask, request
import consul
import sys
import uuid

DATA = {}
app = Flask(__name__)

session = consul.Consul(host='localhost', port=8500)
port = int(sys.argv[1])
session.agent.service.register('logging-service', port=port, service_id=f"logging_{str(uuid.uuid4())}")

client = hazelcast.HazelcastClient()
map = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()


@app.route('/save', methods=["POST"])
def save():
    for k, v in request.json.items():
        try: 
            map.put(k, v).result()
            print(f"Added to hashmap key: {k}, value: {v}")
        except Exception as e:
            return f"Unable to save key {k} with value {v}", 503
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    return ",".join(map.values().result())


if __name__ == '__main__':
    app.run(port=port)
