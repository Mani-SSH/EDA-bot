import json
import os
import nltk
import random

from typing import Dict, List, Tuple, Optional
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

# Download required NLTK data for tokenization, tagging, lemmatization, and stopword handling
nltk.download('punkt', quiet=True)  # Tokenization data
nltk.download('averaged_perceptron_tagger', quiet=True)  # POS tagging model
nltk.download('universal_tagset', quiet=True)  # Tagset for simplified POS tags
nltk.download('wordnet', quiet=True)  # WordNet data for synonym lookup
nltk.download('stopwords', quiet=True)  # List of stopwords

class EDAChatbot:
    def __init__(self, config_path: str = "eda_config.json"):
        #chatbot initialization with config.json
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.config_path = config_path
        self.knowledge_base = self.load_knowledge_base()
        self.keyword_mapping = self._build_keyword_mapping()

    def load_knowledge_base(self)->dict:
        '''Load and Validate the knowledge base from JSON file'''
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"{self.config_path} does not exists")
            
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            return{}
    
    def _build_keyword_mapping(self)->Dict[str,Tuple[str,str]]:
        '''Build a flat mapping of keywords to their categories and subcategories'''
        mapping = {}

        # Process EDA keywords
        for category, content in self.knowledge_base.get("eda_keywords", {}).items():
            # Add main category keywords
            for keyword in content.get("keywords", []):
                mapping[keyword.lower()] = (category, "general")

                # Add synonyms from WordNet
                for syn in wordnet.synsets(keyword):
                    for lemma in syn.lemmas():
                        mapping[lemma.name().lower()] = (category, "general")

            # Process techniques and types
            for subcategory_type in ["techniques", "types"]:
                for subcategory, keywords in content.get(subcategory_type, {}).items():
                    for keyword in keywords:
                        mapping[keyword.lower()] = (category, subcategory)

                        # Add synonyms from WordNet
                        for syn in wordnet.synsets(keyword.split()[0]):  # Use first word for compound terms
                            for lemma in syn.lemmas():
                                mapping[lemma.name().lower()] = (category, subcategory)

        return mapping  


    def extract_keywords(self, message: str) -> List[Tuple[str, str, str]]:
        """Extract keywords and their categories from message"""
        tokens = word_tokenize(message.lower())
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        tagged = pos_tag(lemmatized_tokens, tagset='universal')

        keywords = []
        i = 0
        while i < len(tagged):
            word, pos = tagged[i]

            if word in self.stop_words or len(word) < 3:
                i += 1
                continue

            # Check for compound terms (up to 3 words)
            for n in range(3, 0, -1):
                if i + n <= len(tagged):
                    compound = " ".join(t[0] for t in tagged[i:i+n])
                    if compound in self.keyword_mapping:
                        category, subcategory = self.keyword_mapping[compound]
                        keywords.append((compound, category, subcategory))
                        i += n
                        break
            else:
                # Check single word
                if word in self.keyword_mapping:
                    category, subcategory = self.keyword_mapping[word]
                    keywords.append((word, category, subcategory))
                i += 1

        return keywords

    def get_response(self, message: str, previous_context: Optional[str] = None) -> Tuple[str, bool]:
        """Generate response based on message content"""
        # Check intents first
        message_lower = message.lower()
        for intent in self.knowledge_base.get("intents", []):
            if any(keyword in message_lower for keyword in intent["keywords"]):
                return random.choice(intent["responses"]), False

        # Extract and process keywords
        extracted_keywords = self.extract_keywords(message)
        if extracted_keywords:
            # Group keywords by category
            categories = {}
            for keyword, category, subcategory in extracted_keywords:
                if category not in categories:
                    categories[category] = {}
                if subcategory not in categories[category]:
                    categories[category][subcategory] = []
                categories[category][subcategory].append(keyword)

            # Build response
            response = "I noticed these EDA-related concepts:\n"
            for category, subcategories in categories.items():
                response += f"\n{category.replace('_', ' ').title()}:"
                for subcategory, keywords in subcategories.items():
                    if subcategory != "general":
                        response += f"\n  - {subcategory}: {', '.join(keywords)}"
                    else:
                        response += f" {', '.join(keywords)}"

            # Check for context transitions
            if previous_context:
                transition_key = f"{previous_context}_to_{category}"
                if transition_key in self.knowledge_base.get("context_transitions", {}):
                    response += f"\n\n{random.choice(self.knowledge_base['context_transitions'][transition_key])}"

            return response, True

        return "Could you please provide more details about your data analysis task?", False

    def add_intent(self, name: str, keywords: List[str], responses: List[str]) -> None:
        """Add a new intent to the knowledge base"""
        self.knowledge_base["intents"].append({
            "name": name,
            "keywords": keywords,
            "responses": responses
        })
        self._save_knowledge_base()

    def add_eda_category(self, category: str, keywords: List[str], techniques: Dict[str, List[str]]) -> None:
        """Add a new EDA category with its keywords and techniques"""
        self.knowledge_base["eda_keywords"][category] = {
            "keywords": keywords,
            "techniques": techniques
        }
        self.keyword_mapping = self._build_keyword_mapping()
        self._save_knowledge_base()

    def _save_knowledge_base(self) -> None:
        """Save the current knowledge base to the JSON file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.knowledge_base, f, indent=4, sort_keys=True, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving knowledge base: {str(e)}")