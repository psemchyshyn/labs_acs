from flask import Flask
import hazelcast
import threading
import sys

app = Flask(__name__)
MESSAGES = []


def polling():
    client = hazelcast.HazelcastClient()
    q = client.get_queue("message-queue")
    while True:
        v = q.poll().result()
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
    app.run()
