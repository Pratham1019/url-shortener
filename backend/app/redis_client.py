import redis
from .config import settings

r = redis.from_url(
    settings.redis_url,
    decode_responses=True
)

def check_redis_connection() -> bool:
    try:
        r.ping()
        return True
    except redis.ConnectionError as e:
        raise RuntimeError("Cannot connect to Redis.") from e


def make_key(code: str) -> str:
    return f"short:{code}"


def save_url(code: str, long_url: str, duration: int) -> None:
    r.setex(make_key(code), duration, long_url)


def get_url(code: str) -> str | None:
    url = r.get(make_key(code))
    
    if url is None:
        return None
    
    return str(url)


def short_code_exists(code: str) -> bool:
    return bool(r.exists(make_key(code)))


def delete_url(code: str) -> bool:
    return bool(r.delete(make_key(code)))