import queue
from flask import Flask
import hazelcast
import threading
import sys
import consul
import uuid
import sys

app = Flask(__name__)
MESSAGES = []
port = int(sys.argv[1])

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('messages-service', port=port, service_id=f"messages_{str(uuid.uuid4())}")

def polling():
    client = hazelcast.HazelcastClient()
    q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()
    while True:
        v = q.poll()
        if v is None:
            continue
        print(f"Got: {v}", flush=True)
        MESSAGES.append(v)


@app.route("/retrieve", methods=["GET"])
def retrieve():
    return ",".join(MESSAGES)


t = threading.Thread(target=polling)
t.start()


if __name__ == '__main__':
    app.run(port=port)
