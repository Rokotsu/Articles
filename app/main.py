from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi import FastAPI

from app.config import settings
from app.users.router import router_auth, router_users
from app.articles.router import router_articles as router

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router)



@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")