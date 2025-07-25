from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session 
from models.bloggermodel import createBloggertModel as CBM,updateBloggerModel as UBM
from database.crud import create_blogger,sign_in,edit_blogger,del_blogger,get_all_bloggers,get_a_blogger,get_all_posts
from database.connect import get_db
from auth.hashing import createhash
from auth.oauth import get_blogger
from database.model import Blogger

bloggerRouter = APIRouter(prefix="/User")
  
@bloggerRouter.post("/Sign-up",status_code=status.HTTP_201_CREATED)
async def Create_New_Blogger(blogger: CBM,db:Session = Depends(get_db)):
    hashedpassword = createhash(blogger.password)
    return create_blogger(db = db,uname = blogger.username,fname=blogger.fullname,email=blogger.email,pword = hashedpassword)

@bloggerRouter.post("/Log-in")
def Login (name:str,pword:str,db:Session = Depends(get_db)):
    return sign_in(username=name,password=pword,db=db)
         
@bloggerRouter.patch("/Update")
def Update_Blogger(blogger: UBM,db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
    return edit_blogger(db=db,username= current_blogger.username, update= blogger)

@bloggerRouter.delete("/Delete/{name}",status_code=status.HTTP_204_NO_CONTENT)
def Delete_Blogger(db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   return del_blogger(db=db, blogger_db= current_blogger.username)

@bloggerRouter.get("/Bloggers")
def Get_All_Blogger(db:Session = Depends(get_db)):
   return get_all_bloggers(db = db)

@bloggerRouter.get("/Post-history")
def Post_History(db: Session = Depends(get_db),current_user: Blogger= Depends(get_blogger)):
    return get_all_posts(db=db,current_blogger= current_user)

#search route
@bloggerRouter.get("/Search/By-name/{name}")
def Get_Blogger(name,db:Session = Depends(get_db)):
    return get_a_blogger(name,db=db)

