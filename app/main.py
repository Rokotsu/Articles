from fastapi import FastAPI
from app.users.router import router_auth, router_users
from app.articles.router import router_articles as router

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router)
