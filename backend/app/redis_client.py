import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5
)

def check_redis_connection() -> bool:
    try:
        r.ping()
        return True
    except redis.ConnectionError as e:
        raise RuntimeError("Cannot connect to Redis. ") from e

def make_key(code: str) -> str:
    return f"short:{code}"

def save_url(code: str, long_url: str, duration: int):
    r.setex(make_key(code), duration, long_url)
    
def get_url(code: str):
    return r.get(make_key(code))

def check_if_exists(code: str) -> bool:
    return bool(r.exists(make_key(code)))