import hazelcast
from flask import Flask, request

DATA = {}
app = Flask(__name__)


client = hazelcast.HazelcastClient()
map = client.get_map("map-lock")


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
    app.run()
