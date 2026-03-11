"""FastAPI Application"""

from fastapi import FastAPI

from app.routers.item_listing_routers import router as item_listing_router
<<<<<<< HEAD
from app.routers.restaurants_routers import router as restaurants_router
from app.routers.menu_routers import router as menu_router
=======
from app.routers.auth_router import router as auth_router
>>>>>>> main

app = FastAPI(title="SKMS Backend")

app.include_router(item_listing_router)
<<<<<<< HEAD
app.include_router(restaurants_router)
app.include_router(menu_router)
=======
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
>>>>>>> main
