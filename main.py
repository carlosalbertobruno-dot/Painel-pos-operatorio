from flask import Flask, send_file, request, jsonify
import json, os, requests

app = Flask(__name__)
DATA_FILE = 'progress.json'
TRELLO_KEY = '3956f2efa588dd58ec180973d62379d4'
TRELLO_TOKEN = 'eab2c79f1656bbda3c6c0c7745bc55fe3983992a442d7ff02c6be36f998abb0c'
TRELLO_BASE = 'https://api.trello.com/1'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE,'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    return jsonify(load_data())

@app.route('/api/progress', methods=['POST'])
def set_progress():
    save_data(request.get_json())
    return jsonify({'ok': True})

@app.route('/api/trello/<path:path>')
def trello_proxy(path):
    params = dict(request.args)
    params['key'] = TRELLO_KEY
    params['token'] = TRELLO_TOKEN
    r = requests.get(f'{TRELLO_BASE}/{path}', params=params)
    return jsonify(r.json()), r.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
