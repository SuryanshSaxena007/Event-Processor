from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.db.database import get_db
from app.db.models import User
from app.core.security import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.username == user.username))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(new_user)
    await db.commit()
    return {"message":"User created successfully"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.username == form_data.username))
    user = res.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub":user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}