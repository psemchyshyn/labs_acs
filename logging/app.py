from flask import Flask, request

DATA = {}
app = Flask(__name__)


@app.route('/save', methods=["POST"])
def save():
    for k, v in request.json.items():
        try:
            DATA[k] = v
            print(f"Added to hashmap key: {k}, value: {v}")
        except Exception as e:
            return f"Unable to save key {k} with value {v}", 503
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    return ",".join(DATA.values())


if __name__ == '__main__':
    app.run()
