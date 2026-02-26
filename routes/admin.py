from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Order, MenuItem, User
from auth import require_admin

router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("/revenue")
def total_revenue(db: Session = Depends(get_db)):
    total = db.query(func.sum(Order.total_price)).scalar() or 0
    return {"total_revenue": total}

@router.get("/top-items")
def top_items(db: Session = Depends(get_db)):
    # simple placeholder: return all items sorted by price descending
    return db.query(MenuItem).order_by(MenuItem.price.desc()).all()

@router.get("/active-users")
def active_users(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {"active_users": count}