"""FastAPI Application"""
from fastapi import FastAPI

from app.routers.item_listing_routers import router as item_listing_router
from app.routers.auth_router import router as auth_router
from app.routers.order_router import router as order_router

app = FastAPI(title="SKMS Backend")

app.include_router(item_listing_router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(order_router)