from flask import Flask,request
from models import Schema
from plzService import PLZService

app = Flask(__name__)


@app.route("/create", methods=["POST"])
def createPLZ():
    print(request.get_json())
    return PLZService().create(request.get_json())

if __name__ == "__main__":
    Schema()
    app.run(debug = True)