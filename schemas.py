from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    phone: str
    name: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool
    name: Optional[str]


class UserOut(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Menu ──────────────────────────────────────────────────────────────
class MenuItemCreate(BaseModel):
    name: str
    price: float
    description: str
    emoji: Optional[str] = "☕"


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    is_available: Optional[bool] = None


class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: str
    emoji: str
    is_available: bool

    class Config:
        from_attributes = True


# ── Orders ────────────────────────────────────────────────────────────
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str = "mpesa"


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    menu_item: MenuItemOut

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    total: float
    status: str
    payment_method: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


# ── Dashboard ─────────────────────────────────────────────────────────
class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    active_users: int
    orders_today: int
    weekly_sales: List[dict]
    recent_orders: List[dict]
    top_items: List[dict]
