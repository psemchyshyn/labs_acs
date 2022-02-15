from flask import Flask, request, jsonify

DATA = {}
app = Flask(__name__)


@app.route('/save', methods=["POST"])
def save():
    print(request.json)
    for k, v in request.json.items():
        try:
            DATA[k] = v
        except Exception as e:
            return f"Unable to save key {k} with value {v}", 503
    return "Saved successfully"


@app.route('/retrieve', methods=["GET"])
def retrieve():
    result = []
    for key in request.json['keys']:
        try:
            result.append(DATA[key])
        except KeyError as e:
            return f"No data stored with key {key}", 404
    return jsonify(result)


if __name__ == '__main__':
    app.run()
