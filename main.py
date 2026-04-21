from flask import Flask, send_file, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = 'progress.json'

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
    data = request.get_json()
    save_data(data)
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
