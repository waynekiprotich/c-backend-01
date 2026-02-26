# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, Base, SessionLocal
from auth import hash_password
from routes.auth import router as auth_router
from routes.menu import router as menu_router
from routes.orders import router as orders_router
from routes.admin import router as admin_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Perfect Coffee API")

# CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Vite dev server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(menu_router, prefix="/menu", tags=["menu"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


# Seed admin + default menu items
def seed_data():
    db: Session = SessionLocal()

    # Admin user
    admin_exists = db.query(models.User).filter(models.User.phone == "0700000000").first()
    if not admin_exists:
        admin = models.User(
            phone="0700000000",
            name="Admin",
            hashed_password=hash_password("admin123"),
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("Admin user created: 0700000000 / admin123")
    else:
        print("Admin already exists")

    # Default menu items
    if not db.query(models.MenuItem).first():
        menu_items = [
            models.MenuItem(name="Espresso", price=200, description="Strong and bold espresso"),
            models.MenuItem(name="Latte", price=250, description="Smooth latte with milk"),
            models.MenuItem(name="Cappuccino", price=300, description="Classic cappuccino"),
            models.MenuItem(name="Americano", price=220, description="Espresso with hot water"),
            models.MenuItem(name="Mocha", price=280, description="Chocolate-flavored coffee")
        ]
        db.add_all(menu_items)
        db.commit()
        print("5 default menu items added")
    else:
        print("Menu items already exist")

    db.close()


seed_data()