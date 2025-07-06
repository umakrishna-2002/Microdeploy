from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})

@app.route('/status')
def status():
    return jsonify({"status": "ok", "service": "backend"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
