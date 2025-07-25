from fastapi import  HTTPException,status,Depends, UploadFile, File, Form

from sqlalchemy.orm import Session 
from .model import Blogger,Post,PostFile
from database.connect import get_db
from auth.hashing import verifyhash
from auth.oauth import get_blogger,create_token
from models.bloggermodel import updateBloggerModel as UBM
import os

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
      verifyhash(password,blogger_db.password)
      create_token_credentials = dict
      create_token_credentials = {
           "sub":username
       }
      return create_token(create_token_credentials)

#edit profile
def edit_blogger(update,username:str,db:Session=Depends(get_db)):   
   blogger_db = db.query(Blogger).filter(Blogger.username == username).first()

   if not blogger_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   
   for field,value in update.dict(exclude_unset = True).items():
        setattr(blogger_db,field,value)
        
   db.commit()
   db.refresh(blogger_db)
  
   return blogger_db

#delete profile
def del_blogger(db:Session,blogger_db):
    exist = db.query(Blogger).filter(Blogger.username == blogger_db).first()
    if exist :
        db.delete(exist)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

def get_all_bloggers(db:Session):
    return db.query(Blogger).all()
    
def get_a_blogger(blogger_db,db:Session):
   exist =db.query(Blogger).filter(Blogger.username == blogger_db).first()
   if exist :
      return {
          "username":blogger_db
      }
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# view post history
def get_all_posts(db: Session = Depends(get_db),current_blogger: Blogger= Depends(get_blogger)):
    posts = db.query(Post).filter(Post.author_id == current_blogger.id).all()
    return posts

##post

MAX_TOTAL_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = { ".jpg", ".jpeg", ".png", ".gif",".mp4", ".avi", ".mov",".pdf", ".docx", ".txt"}
async def create_post(title,content,acct_id,uploads=None,db: Session = Depends(get_db)):
   total_size = 0
   saved_files = []

    # Read and validates all files 
   if uploads:
      for file in uploads:
         content_data = await file.read()
         file_size = len(content_data)
         total_size += file_size
         
         if total_size > MAX_TOTAL_SIZE:
                raise HTTPException(status_code=400, detail="Total file size exceeds 10MB limit.")

         _, ext = os.path.splitext(file.filename.lower())
         if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

         saved_files.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "data": content_data
            })

    # Save post
   new_post = Post(title=title, content=content, author_id=acct_id)
   db.add(new_post)
   db.flush()  # Ensure we get post.id

    # Save files validated
   for file in saved_files:
        db_file = PostFile(
            filename=file["filename"],
            content_type=file["content_type"],
            file_data=file["data"],
            post_id=new_post.id
        )
        db.add(db_file)

   db.commit()
   db.refresh(new_post)

   return {"message": "Post created successfully", "post_id": new_post.id}

def get_all(db:Session):
   read= db.query(Post).all()
   return read

def edit_post(post_id:int, updated_data,db:Session=Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   post_query = db.query(Post).filter(Post.id == post_id).first()
   
   if not post_query:
        raise HTTPException(status_code=404, detail="Post not found")

   if post_query.author_id != current_blogger.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")  
   
   for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(post_query, field, value)
    
   db.commit()
   db.refresh(post_query)
   return post_query

def delete_post(post_id:int,db:Session=Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   post_query = db.query(Post).filter(Post.id == post_id).first()
   
   if not post_query:
        raise HTTPException(status_code=404, detail="Post not found")

   if post_query.author_id != current_blogger.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")  
   
   db.delete(post_query)
   db.commit()
   raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
   
    
def get_a_post(post_db,db:Session,):
   exist =db.query(Post).filter(Post.title == post_db).first()
   if exist :
      return {
          "TITLE:": Post.title,
          "CONTENT": Post.content
      }
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
