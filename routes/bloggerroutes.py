from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session 
from models.bloggermodel import createBloggertModel as CBM,updateBloggerModel as UBM
from database.crud import create_blogger,sign_in,edit_blogger,del_blogger,get_all_blogger,get_a_blogger,get_all_posts
from database.connect import get_db
from auth.hashing import createhash
from auth.oauth import get_blogger
from database.model import Blogger

bloggerRouter = APIRouter(prefix="/User")
  
@bloggerRouter.post("/Sign-up",status_code=status.HTTP_201_CREATED)
async def create_new_blogger(blogger: CBM,db:Session = Depends(get_db)):
    hashedpassword = createhash(blogger.password)
    return create_blogger(db = db,uname = blogger.username,fname=blogger.fullname,email=blogger.email,pword = hashedpassword)

@bloggerRouter.post("/Log-in")
async def login (name:str,pword:str,db:Session = Depends(get_db)):
    return await sign_in(username=name,password=pword,db=db)
         
@bloggerRouter.patch("/update")
def update_blogger(blogger: UBM,db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
    return edit_blogger(db=db,username= current_blogger.username, update= blogger)

@bloggerRouter.delete("/delete/{name}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blogger(db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   return del_blogger(db=db, blogger_db= current_blogger.username)

@bloggerRouter.get("/Bloggers")
def getAllBlogger(db:Session = Depends(get_db)):
   return get_all_blogger(db = db)

@bloggerRouter.get("/post-history")
def history(db: Session = Depends(get_db),current_user: Blogger= Depends(get_blogger)):
    return get_all_posts(db=db,current_blogger= current_user)

#search route
@bloggerRouter.get("/by-name/{name}")
def getBlogger(name,db:Session = Depends(get_db)):
    return get_a_blogger(name,db=db)

