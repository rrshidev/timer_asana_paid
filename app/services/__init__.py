from .redis import RedisConnector

from app.settings import redis_settings


rc = RedisConnector(url=redis_settings.states_url)

__all__ = (
    "rc",
)
