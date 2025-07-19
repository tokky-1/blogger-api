from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session 
from database.connect import get_db
from routes import bloggerroutes
from fastapi.security import OAuth2PasswordRequestForm
from database.crud import verify_user
from auth.oauth import create_token
app = FastAPI(title="BLOGGER API", description="has the basic functionality of a blog site and some")

app.include_router(bloggerroutes.bloggerRouter,tags =["Users"] )


@app.post("/token")#,response_model=Token)
async def give_token(formdata:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = verify_user(formdata.username,formdata.password,db = db )
    if user:
        access_token = create_token(data = {"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    return "user not found"
