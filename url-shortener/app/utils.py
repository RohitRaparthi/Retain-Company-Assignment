# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
from urllib.parse import urlparse

def generate_short_code(length=6):
    """Generate a random alphanumeric short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    """Basic URL validation."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

# Optional: Base62 encode if you use integer-based codes in the future
BASE62 = string.ascii_letters + string.digits

def encode_base62(num):
    """Convert an integer to a base62 string."""
    if num == 0:
        return BASE62[0]
    base62 = ''
    while num:
        num, rem = divmod(num, 62)
        base62 = BASE62[rem] + base62
    return base62
