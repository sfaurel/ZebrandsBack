from fastapi import FastAPI

from app.routers.v1 import products, products_analytics

app = FastAPI(title="Products API")

app.include_router(products.router, prefix="/api/v1")
app.include_router(products_analytics.router, prefix="/api/v1")
