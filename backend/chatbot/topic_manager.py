import json
import os
from typing import List, Optional

class Topic_Manager:
    def __init__(self):
        self.topic_index_path = os.path.join(os.path.dirname(__file__),'..','eda_resources','topic_index.json')
        self.topic_index = self._load_topic_index()
        self.topics = self._load_topics()
        self._cache = {}

    def _load_topic_index(self)->dict:
        try:
            if not os.path.exists(self.topic_index_path):
               raise FileExistsError(f"{self.topic_index_path} does not exists")
           
            with open(self.topic_index_path, 'r') as f:
                return json.load(f)

        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            return{}
    
    def _load_topics(self)->List[str]:
        topics = []

        for topic in self.topic_index.get("available_topics",{}).values():
            topics.extend(topic)

        return list(set(topics))

    
