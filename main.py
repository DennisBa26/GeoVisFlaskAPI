from flask import Flask,request,jsonify
from models import Schema
from plzService import PLZService

app = Flask(__name__)


@app.route("/", methods=["POST"])
def createPLZ():
    print(request.get_json())
    return PLZService().create(request.get_json())

@app.route("/", methods=["GET"])
def getPLZ():
    return jsonify(PLZService().get_all())

if __name__ == "__main__":
    Schema()
    app.run(debug = True)