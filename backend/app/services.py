import random
import string

from .redis_client import save_url, check_if_exists

def generate_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_unique_code() -> str:
    while True:
        code = generate_code()

        if not check_if_exists(code):
            return code


def create_short_url(long_url: str, duration: int = 86400) -> str:
    code = generate_unique_code()
    save_url(code, long_url, duration)
    
    return code
