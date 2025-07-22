from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session 
from fastapi.security import OAuth2PasswordRequestForm
from models.bloggermodel import createBloggertModel as CBM,updateBloggerModel as UBM
from database.crud import create_blogger,sign_in,edit_blogger,del_blogger,get_all_blogger,get_a_blogger,get_all_posts,verify_user
from database.connect import get_db
from auth.hashing import createhash
from auth.oauth import get_blogger, create_token
from database.model import Blogger
bloggerRouter = APIRouter(prefix="/User")

  
@bloggerRouter.post("/Sign-in",status_code=status.HTTP_201_CREATED)
async def create_new_blogger(blogger: CBM,db:Session = Depends(get_db)):
    hashedpassword = createhash(blogger.password)
    return create_blogger(db = db,uname = blogger.username,fname=blogger.fullname,email=blogger.email,pword = hashedpassword)

@bloggerRouter.post("/token")
async def give_token(formdata:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = verify_user(formdata.username,formdata.password,db = db )
    if user:
        access_token = create_token(data = {"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    return "user not found"

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