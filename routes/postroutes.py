from fastapi import APIRouter,status,HTTPException,Depends,Form,File,UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session 
from models.postmodel import postModel as PM,updatePostModel as UPM 
from database.crud import create_post,get_all_post,edit_post,delete_post
from database.connect import get_db
from auth.oauth import get_blogger
from database.model import Post,Blogger

postRouter = APIRouter(prefix="/Post")
@postRouter.post("/create",status_code=status.HTTP_201_CREATED)
async def create_new_post(
    title: str = Form(...),
    content: Optional[str] = Form(None),
    uploads: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_blogger: Blogger = Depends(get_blogger)):
    
    return await create_post(db = db,title=title,content=content,uploads=uploads,acct_id=current_blogger.id)

         
@postRouter.patch("/update")
def update_post(id:int,post:UPM,db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
    return edit_post(post_id = id,updated_data=post,db=db,current_blogger=current_blogger)

@postRouter.delete("/delete/{name}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   return delete_post(db=db, blogger_db= current_blogger.username)


@postRouter.get("/read")
def get_all(db:Session = Depends(get_db)):
   return get_all_post(db = db)