# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

PORT = os.getenv('BACKEND_PORT', 3000)

@app.route('/')
def hello_world():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    app.run(debug=True, port=PORT)  # Keep your backend on port 3000
