import nltk
from nltk.corpus import wordnet,stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('universal_tagset', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

# Sample intents for the chatbot
intents = {
    "greetings": ["hello", "hi", "how are you"],
    "goodbyes": ["bye", "goodbye", "see you"],
    "thanks": ["thank you", "thanks"]
}


# List of EDA-specific keywords
eda_keywords = [
    "clustering", "k-means", "hierarchical", "dbscan",
    "dimensionality reduction", "pca", "t-sne",
    "correlation", "covariance", "regression",
    "visualization", "scatter plot", "histogram", "box plot",
    "outlier detection", "anomaly detection",
    "feature selection", "feature engineering",
    "statistical analysis", "hypothesis testing",
    "data cleaning", "data preprocessing",
    "exploratory data analysis", "eda"
]

def extract_keywords(message):
    try:
        # Tokenize the message
        tokens = word_tokenize(message.lower())
        
        # Tag the tokens with parts of speech
        tagged = pos_tag(tokens, tagset='universal')
        
        # Extract nouns, adjectives, and numbers, excluding stopwords
        keywords = []
        i = 0
        while i < len(tagged):
            word, pos = tagged[i]
            
            # Skip stopwords and very short words (e.g., "me")
            if word in stop_words or len(word) < 3:
                i += 1
                continue
            
            # Check for compound terms (e.g., "k-means", "decision tree")
            if i < len(tagged) - 1:
                next_word, next_pos = tagged[i+1]
                compound = f"{word} {next_word}"
                if compound in eda_keywords:
                    keywords.append(compound)
                    i += 2
                    continue
            
            # Check if the word matches known EDA-related keywords
            if word in eda_keywords:
                keywords.append(word)
            elif '-' in word or (pos in ('NOUN', 'ADJ') and word.isdigit() == False):
                # Add hyphenated terms, nouns, and adjectives
                keywords.append(word)
            
            i += 1
        
        # Remove duplicates while preserving order
        keywords = list(dict.fromkeys(keywords))
        
        return keywords
    except Exception as e:
        print(f"Error in extract_keywords: {str(e)}")
        return []


# Function to respond to user input
def get_response(message):
    try:
        response = "I'm not sure how to respond to that."
        is_eda_related = False

        # Check for keywords in the message
        for intent, keywords in intents.items():
            if any(keyword in message.lower() for keyword in keywords):
                if intent == "greetings":
                    response = "Hi there! How can I assist you with your data analysis?"
                elif intent == "goodbyes":
                    response = "Goodbye! I hope I was helpful with your EDA tasks."
                elif intent == "thanks":
                    response = "You're welcome! Let me know if you need any more help with your analysis."
                break
        else:
            # If no intent is matched, extract keywords
            extracted_keywords = extract_keywords(message)
            eda_related_keywords = [keyword for keyword in extracted_keywords if keyword in eda_keywords]
            
            if eda_related_keywords:
                response = f"I noticed these EDA-related keywords in your message: {', '.join(eda_related_keywords)}."
                is_eda_related = True
            elif extracted_keywords:
                response = f"I noticed these keywords related to your analysis: {', '.join(extracted_keywords)}.<br>Could you provide more context about your data analysis task?"
            else:
                response = "I couldn't find any notable keywords in your message. <br> Could you please provide more details about your data analysis task?"

        return response, is_eda_related
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        return "I'm sorry, but I encountered an error while processing your message.", False
