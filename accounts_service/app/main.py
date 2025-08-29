from fastapi import FastAPI
from app.routers.v1 import auth, accounts


app = FastAPI(title="Accounts API")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
