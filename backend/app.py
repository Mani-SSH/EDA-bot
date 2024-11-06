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
        previous_context = data.get('previousContext')
        
        # Get the response from the chat function
        response_message, is_eda_related, new_context = chatbot.get_response(
            message = message,
            previous_context = previous_context
        )

        # Extract keywords for the response
        extracted_keywords = [
            keyword for keyword, _, _ in chatbot.extract_keywords(message)
        ]

        # Return the response as JSON
        return jsonify({
            "response": response_message,
            "is_eda_related": is_eda_related,
            "context": new_context,
            "keywords": extracted_keywords
        })
    except Exception as e:
        # Log and return an error if something goes wrong
        import traceback
        print(f"Error in receive_message: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e)
        }), 500
    

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    # Run the app
    app.run(debug=True, port=PORT, host='0.0.0.0')
