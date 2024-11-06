import json
import os
import nltk
import random

from typing import Dict, List, Tuple, Optional
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

from .topic_manager import Topic_Manager
# Download required NLTK data for tokenization, tagging, lemmatization, and stopword handling
nltk.download('punkt', quiet=True)  # Tokenization data
nltk.download('averaged_perceptron_tagger', quiet=True)  # POS tagging model
nltk.download('universal_tagset', quiet=True)  # Tagset for simplified POS tags
nltk.download('wordnet', quiet=True)  # WordNet data for synonym lookup
nltk.download('stopwords', quiet=True)  # List of stopwords
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

class EDAChatbot:
    def __init__(self, knowledge_base_path: str = "eda_knowledge_base.json"):
        #chatbot initialization with eda_knowledge_base
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.knowledge_base_path =  os.path.join(os.path.dirname(__file__), "eda_knowledge_base.json")
        self.knowledge_base = self.load_knowledge_base()
        self.keyword_mapping = self._build_keyword_mapping()

    def load_knowledge_base(self)->dict:
        '''Load and Validate the knowledge base from JSON file'''
        try:
            if not os.path.exists(self.knowledge_base_path):
                raise FileNotFoundError(f"{self.knowledge_base_path} does not exists")
            
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            return{}
    
    def _build_keyword_mapping(self)->Dict[str,Tuple[str,str]]:
        '''Build a flat mapping of keywords to their categories and subcategories'''
        mapping = {}

        # Process eda_keywords from the json file
        # Example of "eda_keywords" structure in the JSON:
        # {
        #     "data_cleaning": {
        #         "keywords": ["clean", "preprocess", "prepare"],
        #         "techniques": {
        #             "missing_values": ["null", "missing data", "empty"],
        #             "outliers": ["outlier detection", "anomaly"],
        #         }
        #     }
        # }
        # In this example:
        # - "data_cleaning" is the category
        # - "clean", "preprocess", and "prepare" are main category keywords
        # - "missing_values" and "outliers" are subcategories under "techniques"
        # - "null", "missing data", and "empty" are keywords under "missing_values"

        for category, content in self.knowledge_base.get("eda_keywords",{}).items():

            #Add main category, i.e "keywords" from json file 
            for keyword in content.get("keywords",[]):
                mapping[keyword.lower()] = (category,"general")
            
                #Add synonyms from WordNet for "keywords"
                for syn in wordnet.synsets(keyword):
                    for lemma in syn.lemmas():
                        mapping[lemma.name().lower] = (category,"general")
            
            #Add sub-categories, i.e. "techniques" and "types" from the json file
            for subcategory_type in ["techniques","types"]:
                for subcategory, keywords in content.get(subcategory_type,{}).items():
                    for keyword in keywords:
                        mapping[keyword.lower()] = (category, subcategory)

                        no_space = keyword.replace(" ", "")
                        with_hyphen = keyword.replace(" ", "-")
                        mapping[no_space.lower()] = (category, subcategory)
                        mapping[with_hyphen.lower()] = (category, subcategory)

        # mapping will be:
        #{
        # "clean": ("data_cleaning", "general"),
        # "neat": ("data_cleaning", "general"),       # Example synonym for "clean"
        # "preprocess": ("data_cleaning", "general"),
        # "prepare": ("data_cleaning", "general"),
        # "ready": ("data_cleaning", "general"),      # Example synonym for "prepare"
        # "null": ("data_cleaning", "missing_values"),
        # "void": ("data_cleaning", "missing_values"), # Example synonym for "null"
        # "missing data": ("data_cleaning", "missing_values"),
        # "empty": ("data_cleaning", "missing_values"),
        # "absent": ("data_cleaning", "missing_values"), # Example synonym for "empty"
        # "outlier detection": ("data_cleaning", "outliers"),
        # "anomaly": ("data_cleaning", "outliers")
        # }
        return mapping
        



    def extract_keywords(self, message: str) -> List[Tuple[str, str, str]]:
        '''
        Extract keywords and their categories from the provided message.

        Parameters:
        - message (str): The input message from which keywords will be extracted.

        Returns:
        - List[Tuple[str, str, str]]: A list of tuples where each tuple contains:
            - The keyword (str),
            - The category (str),
            - The subcategory (str).

        Example:
        - message : "I need help with data cleaning and analysis."
        - self.keyword_mapping = {
                "data cleaning": ("Data Preparation", "Techniques"),
                "data analysis": ("Data Analysis", "Techniques"),
                "help": ("Assistance", "General"),
            }
        - keywords : [
                ('help', 'Assistance', 'General'),
                ('data cleaning', 'Data Preparation', 'Techniques'),
                ('data analysis', 'Data Analysis', 'Techniques')
            ]
        '''

        # Tokenize the lowercased message into individual words
        tokens = word_tokenize(message.lower())
        
        # Lemmatize tokens, e.g., 'running' -> 'run' (lemma)
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        # Tag the lemmatized tokens with their part of speech, e.g., 'the red' -> [('the', 'DET'), ('red', 'ADJ')]
        tagged = pos_tag(lemmatized_tokens, tagset='universal')

        keywords = []
        i = 0

        while i < len(tagged):
            word, pos = tagged[i]  # Get the current word and its POS tag

            # Skip words that are stop words (e.g., 'and', 'the') or have fewer than 3 characters
            if word in self.stop_words or len(word) < 3:
                i += 1
                continue
            
            # Check for compound terms (up to 3 words)
            for n in range(3, 0, -1):
                if i + n <= len(tagged):
                    compound = " ".join(t[0] for t in tagged[i:i+n])  # Form the compound phrase
                    if compound in self.keyword_mapping:
                        category, subcategory = self.keyword_mapping[compound]
                        keywords.append((compound, category, subcategory))  # Add compound keyword to the list
                        i += n  # Move index forward by the number of words in the compound
                        break
            else:
                # Check for single word keywords
                if word in self.keyword_mapping:
                    category, subcategory = self.keyword_mapping[word]
                    keywords.append((word, category, subcategory))  # Add single word keyword to the list
                i += 1  # Move to the next word

        return keywords  # Return the list of extracted keywords
    


    def get_response(self, message: str, previous_context: Optional[str] = None) -> Tuple[str, bool, Optional[str]]:
        '''Generate response based on message content'''
        message_lower = message.lower()

        try:
            topic_manager = Topic_Manager()

            if previous_context:
                try:
                    prev_topics = json.loads(previous_context)
                    # Check for general affirmative responses
                    affirmative_words = {'yes', 'yeah', 'sure', 'okay', 'please', 'tell', 'explain'}
                    if any(word in message_lower for word in affirmative_words):
                        # If only one topic was offered, explain that topic
                        if len(prev_topics) == 1:
                            topic = prev_topics[0]
                            explanation = f"I have got the explanation {previous_context} please wait..."
                            return explanation, True, None  # Clear context after explaining
                    
                    # Check if user mentioned a specific topic
                    for topic in prev_topics:
                        if topic.lower() in message_lower:
                            explanation = f"Hello I see I will be reaching out to you soon {previous_context}"
                            return explanation, True, None  # Clear context after explaining
                except json.JSONDecodeError:
                    print(f"Invalid context format: {previous_context}")
                    pass  # Invalid context, process as new query

            found_topics = set()
            
            # Check intents first
            for intent in self.knowledge_base.get("intents", []):
                # print(f"Intent detected: {intent['name']}")  # Debugging
                if any(keyword in message_lower for keyword in intent["keywords"]):
                    return random.choice(intent["responses"]), False, None

            # Extract and process the keywords
            extracted_keywords = self.extract_keywords(message)

            # Check for the extracted_keywords in message
            if not extracted_keywords:
                return "Could you please provide more details about your data analysis task?", False, None
                         
            # Group keywords by category
            '''
            Example: 
            extracted_keywords = [
                ('help', 'Assistance', 'General'),
                ('data cleaning', 'Data Preparation', 'Techniques'),
                ('data analysis', 'Data Analysis', 'Techniques')
            ]

            categories = {
                'Assistance': {
                    'General': ['help']
                },
                'Data Preparation': {
                    'Techniques': ['data cleaning']
                },
                'Data Analysis': {
                    'Techniques': ['data analysis']
                }
            }
            '''
            categories = {}
            for keyword, category, subcategory in extracted_keywords:
                if category not in categories:
                    categories[category] = {}
                if subcategory not in categories[category]:
                    categories[category][subcategory] = []
                categories[category][subcategory].append(keyword)

                # Check for available topics in topic_manager
                if subcategory in topic_manager.topics:
                    found_topics.add(subcategory)
                if category in topic_manager.topics:
                    found_topics.add(category)
            

            '''Building response'''
            # build initial response 
            phrases = self.knowledge_base.get("phrases",[])
            initial_phrase = random.choice(phrases)
            
            response = f"{initial_phrase} {len(extracted_keywords)} EDA-related concept{'s' if len(extracted_keywords)>1 else ''}:\n"

            for category, subcategories in categories.items():
                category_title = category.replace('_', ' ').title()
                response += f"📊 {category_title}:\n"
                
                for subcategory, keywords in subcategories.items():
                    keyword_str = ", ".join(f'"{k}"' for k in keywords)
                    if subcategory != "general":
                        subcategory_title = subcategory.replace('_', ' ').title()
                        response += f"• {keyword_str} ({subcategory_title})\n"
                    else:
                        response += f"• {keyword_str} \n"
    
            response += "\n"

            
            if found_topics:
                response += f"I have information on these topics: {', '.join(found_topics).title()}\n"
                response += "Let me know if you'd like to dive deeper into any of these!"
            else:
                response += "Sorry, but I cannot help you with this specific topic"

            context_for_frontend = None
            if found_topics:
                context_for_frontend = json.dumps(list(found_topics))

            # Return the final response
            return response, True, context_for_frontend

        
        except Exception as e:
            print(f"Error in get_resposne: {str(e)}")
            return "I am having trouble processing your request right now.", False, None
        