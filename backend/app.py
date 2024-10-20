import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import get_response

load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = os.getenv('BACKEND_PORT', 3000)

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.json
        message = data.get('message')

        print(f'Message: {message}')
        
        # Get response from chatbot
        response_message, is_eda_related = get_response(message)

        return jsonify({
            "response": response_message,
            "is_eda_related": is_eda_related
        })
    except Exception as e:
        print(f"Error in receive_message: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT)