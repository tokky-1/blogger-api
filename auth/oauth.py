from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.model import Blogger
from database.connect import get_db
from dotenv import load_dotenv
import os,time

import logging

load_dotenv(override=True)

KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP = os.getenv("EXPIRE")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token: str = Depends(oauth2_scheme)
headers = {
    "Authorization": f"Bearer {token}"
}


def create_token(data: dict):
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=float(EXP))
    payload.update({"exp":expire.timestamp()})
    token = jwt.encode(payload, KEY, algorithm=ALGORITHM)
    return token


def get_blogger(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:     
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        print (f"payload is " + payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Blogger).filter(Blogger.username == username).first()
    if user is None:
        raise credentials_exception
    return user