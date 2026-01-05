from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserResponse
from database import SessionLocal
import logging

router = APIRouter()

# Logging setup
logger = logging.getLogger(__name__)

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.remove()

@router.post("/auth/signup", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password_hash=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created: {db_user.username}")
    return db_user

@router.post("/auth/login")
async def login_user(user: UserCreate):
    # Implement login logic here
    raise HTTPException(status_code=200, detail="Login logic not implemented")
