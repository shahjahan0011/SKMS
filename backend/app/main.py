"""FastAPI Application"""

from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.order_router import router as order_router
from backend.app.routers.item_listing_router import router as item_listing_router
from backend.app.routers.menu_router import router as menu_router
from app.routers.delivery_router import router as delivery_router
from app.routers.payment_router import router as payment_router
from app.routers.notification_router import router as notification_router
from app.routers.cost_router import router as cost_router

app = FastAPI(title="SKMS Backend", redirect_slashes=True)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(delivery_router, tags=["Deliveries & Locations"])
app.include_router(menu_router, tags=["Menus"])
app.include_router(order_router, tags=["Orders"])

app.include_router(item_listing_router, tags=["Item Listings"])
app.include_router(payment_router, tags=["Payments"])

app.include_router(notification_router, tags=["Notifications"])
app.include_router(cost_router, prefix="/cost", tags=["Cost"])

@app.on_event("startup")
def log_routes():
    print("\n=== REGISTERED ROUTES ===")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"Path: {route.path} | Methods: {route.methods}")
    print("=========================\n")
