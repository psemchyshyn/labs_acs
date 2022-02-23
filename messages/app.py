from flask import Flask


app = Flask(__name__)


@app.route("/retrieve", methods=["GET"])
def retrieve():
    return "Not implemented yet"


if __name__ == '__main__':
    app.run()
