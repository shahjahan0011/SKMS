"""FastAPI Application"""
from fastapi import FastAPI

from app.routers.auth_router import router as auth_router

app = FastAPI(title="SKMS Backend")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])