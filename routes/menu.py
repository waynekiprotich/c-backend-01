from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MenuItem
from auth import require_admin

router = APIRouter()

# Public menu
@router.get("/")
def get_menu(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

# Admin CRUD
@router.post("/", dependencies=[Depends(require_admin)])
def create_menu_item(name: str, price: float, db: Session = Depends(get_db)):
    item = MenuItem(name=name, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{item_id}", dependencies=[Depends(require_admin)])
def update_menu_item(item_id: int, name: str, price: float, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = name
    item.price = price
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", dependencies=[Depends(require_admin)])
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item deleted"}