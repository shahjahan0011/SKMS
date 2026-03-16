"""FastAPI Application"""

from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.order_router import router as order_router
from app.routers.item_listing_routers import router as item_listing_router
from app.routers.restaurants_routers import router as restaurants_router
from app.routers.menu_routers import router as menu_router
from app.routers.delivery_router import router as delivery_router


app = FastAPI(title="SKMS Backend", redirect_slashes=True)

app.include_router(delivery_router, tags=["Deliveries"])
app.include_router(menu_router, tags=["Menus"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(order_router)
app.include_router(item_listing_router)
app.include_router(restaurants_router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(delivery_router, prefix="/locations", tags=["Locations"])
app.include_router(item_listing_router, tags=["Restaurants"])

@app.on_event("startup")
def log_routes():
    print("\n=== REGISTERED ROUTES ===")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"Path: {route.path} | Methods: {route.methods}")
    print("=========================\n")
