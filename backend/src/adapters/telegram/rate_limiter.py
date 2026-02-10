import time

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def is_allowed(self, user_id: int, max_requests: int = 10, window_seconds: int = 60) -> bool:
        key = f"rate_limit:{user_id}"
        now = time.time()
        await self.redis.zremrangebyscore(key, 0, now - window_seconds)
        request_count = await self.redis.zcard(key)
        return request_count < max_requests

    async def increment(self, user_id: int):
        key = f"rate_limit:{user_id}"
        now = time.time()
        await self.redis.zadd(key, {str(now): now})
        await self.redis.expire(key, 3600)
