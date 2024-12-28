from flask import Flask
from models import Schema

app = Flask(__name__)


@app.route("/")
def getData():
    return "data"

if __name__ == "__main__":
    Schema()
    app.run(debug = True)