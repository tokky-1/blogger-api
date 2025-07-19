from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session 
from models.bloggermodel import createBloggertModel as CBM
from database.crud import create_blogger,sign_in
from database.connect import get_db
from auth.hashing import createhash
from auth.oauth import get_blogger
bloggerRouter = APIRouter(prefix="/User")

  
@bloggerRouter.post("/createBlogger",status_code=status.HTTP_201_CREATED)
async def create_new_blogger(blogger : CBM,db:Session = Depends(get_db)):
    hashedpassword = createhash(blogger.password)
    return create_blogger(db = db,uname = blogger.username,fname=blogger.fullname,email=blogger.email,pword = hashedpassword)

@bloggerRouter.post("/login")
def login (name:str,pword:str,db:Session = Depends(get_db)):
    return sign_in(username=name,password=pword,db=db)