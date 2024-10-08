import nltk
nltk.download('punkt')
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = os.getenv('BACKEND_PORT', 3000)
lemmatizer = WordNetLemmatizer()

# Sample intents for the chatbot
intents = {
    "greetings": ["hello", "hi", "how are you"],
    "goodbyes": ["bye", "goodbye", "see you"],
    "thanks": ["thank you", "thanks"]
}

# Function to respond to user input
def get_response(message):
    # Preprocess the message
    tokens = nltk.word_tokenize(message.lower())
    response = "I'm not sure how to respond to that."

    # Check for keywords in the message
    for intent, keywords in intents.items():
        if any(word in tokens for word in keywords):
            if intent == "greetings":
                response = "Hi there! How can I assist you?"
            elif intent == "goodbyes":
                response = "Goodbye! Have a great day!"
            elif intent == "thanks":
                response = "You're welcome! Let me know if you need anything else."
            break

    return response

@app.route('/send-message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message')

    print(f'Message: {message}')
    
    # Get response from chatbot
    response_message = get_response(message)

    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
