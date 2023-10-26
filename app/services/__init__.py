from .redis import RedisStorage as RS

from app.settings import redis_settings

RedisStorage = RS(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)

__all__ = ("RedisStorage",)
