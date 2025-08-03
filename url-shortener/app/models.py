# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

import time
import threading
import random
import string

class URLStore:
    def __init__(self):
        self.url_map = {}  # short_code -> {"url": ..., "clicks": ..., "created_at": ...}
        self.lock = threading.Lock()

    def _generate_short_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def shorten_url(self, original_url):
        with self.lock:
            short_code = self._generate_short_code()
            while short_code in self.url_map:
                short_code = self._generate_short_code()

            self.url_map[short_code] = {
                "url": original_url,
                "clicks": 0,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            return short_code

    def get_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]["clicks"] += 1
                return True
            return False

    def get_stats(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)
