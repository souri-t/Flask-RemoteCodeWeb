from urllib import response
from flask import Flask, jsonify
import requests, json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

URL = "http://192.168.31.198:8080"

@app.route('/')
def index():
    return jsonify({
        "message": "API Only"
    })
    
@app.route('/Appliances')
def GetAppliances():
    headers = {"content-type": "application/json"}
    response = requests.get(f'{URL}/api/rest/remote/appliances', headers=headers)

    data = response.json()
    # return json.dumps(data["appliances"], indent=2, ensure_ascii=False)
    return data

@app.route('/Appliances/<int:appliance_id>/Commands', methods=['GET'])
def GetCommands(appliance_id=None):
    headers = {"content-type": "application/json"}
    response = requests.get(f'{URL}/api/rest/remote/appliances/{appliance_id}/commands', headers=headers)
    return response.json()

@app.route('/Remote/Commands/<int:command_id>', methods=['POST'])
def SendCommand(command_id=None):
    return { 'text' : command_id }

if __name__ == '__main__':
  app.run()
