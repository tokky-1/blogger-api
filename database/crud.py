from fastapi import  HTTPException,status,Depends
from sqlalchemy.orm import Session 
from .model import Blogger,Post
from database.connect import get_db
from auth.hashing import verifyhash

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
