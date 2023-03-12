from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from jose import jwt
from passlib.context import CryptContext
from controller import userController
from sqlalchemy.orm import Session
from typing import Union
from database.connection import get_db
from security.cookie import OAuth2PasswordBearerWithCookie
from fastapi import Depends, APIRouter, Request, Response, status


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
COOKIE_NAME = "Authorization"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="signin")

authRouter = APIRouter()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],)
    user: str = userController.get_user_by_username(
        db=db, username=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.username


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],)
    user: str = userController.get_user_by_username(db=db, username=payload.get("sub"))
    if user and user.is_Admin==True:
        return user.username
    else:
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/signin"})
