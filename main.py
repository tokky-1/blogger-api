from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from routes import bloggerroutes,postroutes
from middleware import ratelimit
from fastapi.security import OAuth2PasswordRequestForm
from database.connect import get_db
from database.crud import verify_user
from auth.oauth import  create_token

import os

app = FastAPI(title="BLOGGER API", description="has the basic functionality of a blog site ")

port = int(os.environ.get("PORT",5001))

app.add_middleware(ratelimit)
app.include_router(bloggerroutes.bloggerRouter,tags =["Users"] )
app.include_router(postroutes.postRouter,tags=["Posts"])

 
@app.post("/token")
async def give_token(formdata:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = verify_user(formdata.username,formdata.password,db = db )
    if user:
        access_token = create_token(data = {"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")