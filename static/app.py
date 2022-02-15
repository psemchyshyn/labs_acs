from flask import Flask


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def do_something():
    return "EMPTY"


if __name__ == '__main__':
    app.run()
