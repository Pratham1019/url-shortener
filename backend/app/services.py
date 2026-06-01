import random
import string
from .redis_client import get_url, save_url, short_code_exists, delete_url


def generate_unique_code(length: int = 6) -> str:
    """Generate an unused short code."""
    while True:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=length))

        if not short_code_exists(code):
            return code

def create_short_code(long_url: str, duration: int = 86400) -> str:
    """Create and store a short code."""
    code = generate_unique_code()

    save_url(code, long_url, duration) # Save it to redis
    return code

def get_long_url(code: str) -> str | None:
    """Return the original URL for a short code."""
    return get_url(code)

def delete_short_code(code: str) -> bool:
    """Delete a short code."""
    return delete_url(code)