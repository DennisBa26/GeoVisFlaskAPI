from flask import Flask,request,jsonify
from models import Schema
from plzService import PLZService
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def getPLZ():
    json_response = jsonify(PLZService().get_all())
    formatted_data = {
        "PLZ_PV": [
            {"PLZ": str(entry[0]), "PV": str(entry[1])} for entry in json_response.get_json()
        ]
    }
    return json.dumps(formatted_data, indent=4)


if __name__ == "__main__":
    Schema()
    app.run(debug = True)