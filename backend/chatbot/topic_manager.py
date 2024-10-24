import json
import os
from typing import List, Optional

class Topic_Manager:
    def __init__(self, topic_dir:str = "../eda_topics/"):
        self.topic_dir = topic_dir
        self.topic_index = self._load_topic_index()
        self._cache = {}

    def _load_topic_index(self)->List[str]:
        topic_files = [
            file_name for file_name in os.listdir(self.topic_dir)
            if file_name.endswith('.json')
        ]
        return topic_files
    
dummy = Topic_Manager()

print(dummy.topic_index)