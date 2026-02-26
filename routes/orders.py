from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order, MenuItem, User
from auth import get_current_user, require_admin

router = APIRouter()

# Place order
@router.post("/")
def place_order(item_ids: list[int], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(MenuItem).filter(MenuItem.id.in_(item_ids)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No valid items found")
    total = sum(item.price for item in items)
    order = Order(user_id=current_user.id, total_price=total)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"order_id": order.id, "total_price": total}

# View my orders
@router.get("/my-orders")
def my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

# Admin view all orders
@router.get("/", dependencies=[Depends(require_admin)])
def all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()