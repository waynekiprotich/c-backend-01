from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register")
def register(phone: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    hashed = hash_password(password)
    user = User(phone=phone, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "phone": user.phone, "role": user.role}

@router.post("/login")
def login(phone: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "phone": current_user.phone, "role": current_user.role}