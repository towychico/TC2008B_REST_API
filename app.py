from flask import Flask, jsonify,request,abort
import json
import os
from dotenv import load_dotenv

load_dotenv()
JSON_FILE = "data.json"


app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

def read_json():

    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"error": "JSON file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON"}


@app.before_request
def before_request():
    client_key = request.headers.get("X-API-KEY")
    if not(client_key) or client_key != API_KEY:
        abort(401,description="Unauthorized: invalid or missing API key")
# GET: Devuelve el contenido de data.json
@app.get('/simulation_data')
def get_whole_simulation_data():
    data = read_json()
    return jsonify(data)
@app.get('/simulation_data/states')
def get_simulation_states():
    data = read_json()
    return jsonify(data['agent_states'])

@app.get('/simulation_data/number_of_steps')
def get_simulation_number_of_steps():
    data = read_json()
    return jsonify(data['steps'])



@app.post('/simulation_data')
def add_whole_simulation():
    new_data =request.get_json()
    if not(new_data):
        abort(404,description="Bad Request: no JSON body provided")

    with open(JSON_FILE, "w") as file:
        json.dump(new_data, file,indent=4)

    return jsonify({"message": "simulation data saved successfully"}),201


if __name__ == '__main__':
    app.run()
