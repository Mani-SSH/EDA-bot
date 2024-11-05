import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from chatbot.chat_module import EDAChatbot # Import the get_response function from chat.py

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/send-message": {"origins": "*"}})

# Set the port, defaulting to 3000 if BACKEND_PORT is not set
PORT = int(os.getenv('BACKEND_PORT', 3000))

chatbot = EDAChatbot()

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        # Get the message from the request
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message']
        # print(f'Received message: {message}')
        
        # Get the response from the chat function
        response_message, is_eda_related = chatbot.get_response(message)

        # Return the response as JSON
        return jsonify({
            "response": response_message,
            "is_eda_related": is_eda_related
        })
    except Exception as e:
        # Log and return an error if something goes wrong
        print(f"Error in receive_message: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, port=PORT)
