from fastapi import  HTTPException,status,Depends
from sqlalchemy.orm import Session 
from .model import Blogger,Post
from database.connect import get_db
from auth.hashing import verifyhash
from auth.oauth import get_blogger
from models.bloggermodel import updateBloggerModel as UBM


def verify_user(username:str,password:str,db:Session = Depends(get_db)):
   blogger = db.query(Blogger).filter(Blogger.username == username).first()
   if blogger:
      hash = verifyhash(password,blogger.password)
      if not hash:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
      return blogger
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid user")


#create blogger
def create_blogger(db:Session,uname:str,fname:str,email:str,pword:str):
    email_check = db.query(Blogger).filter(Blogger.email == email ).first()
    if email_check:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email already exists")
    name_check = db.query(Blogger).filter(Blogger.username == uname ).first()
    if name_check:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exists")
    
    blogger_db = Blogger(username = uname,fullname = fname,email = email,password = pword) 
    
    db.add(blogger_db)
    db.commit()
    db.refresh(blogger_db)
    
    db.close()

    return blogger_db 

#login
def sign_in(username:str,password:str , db:Session = Depends(get_db)):
   blogger_db = db.query(Blogger).filter(Blogger.username == username).first()
   if blogger_db:
        return verifyhash(password,blogger_db.password)

#edit profile
def edit_blogger(update,username:str,db:Session=Depends(get_db)):
   blogger_db = db.query(Blogger).filter(Blogger.username == username).first()
   if not blogger_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   for field,value in update.dict(exclude_unset = True).items():
        setattr(blogger_db,field,value)
   db.commit()
   db.add(blogger_db)
  
   return blogger_db

#delete profile
def del_blogger(db:Session,db_user:int):
    exist = db.query(Blogger).filter(Blogger.id == db_user ).first()
    if exist :
        db.delete(exist)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

def get_all_blogger(db:Session):
    return db.query(Blogger).all()
    