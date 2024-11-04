import json
import os

class URLStorage:
    url_file = "stream_url.json"

    @classmethod
    def load_url(cls):
        if os.path.exists(cls.url_file):
            with open(cls.url_file, 'r') as file:
                data = json.load(file)
                return data.get("url", "")
        return ""

    @classmethod
    def save_url(cls, url):
        with open(cls.url_file, 'w') as file:
            json.dump({"url": url}, file)