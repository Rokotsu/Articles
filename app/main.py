from fastapi import FastAPI
from app.users.router import router_auth, router_users

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
