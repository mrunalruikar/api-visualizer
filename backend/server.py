from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # This line enables CORS for all routes

@app.route('/api/data')
def get_data():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) # Use a different port to avoid conflicts
