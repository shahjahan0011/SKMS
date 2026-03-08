"""FastAPI Application"""
from fastapi import FastAPI
from app.routers.item_listing_routers import router as item_listing_router

app = FastAPI(title="SKMS Backend")

app.include_router(item_listing_router)