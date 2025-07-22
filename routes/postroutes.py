from fastapi import APIRouter,status,HTTPException,Depends,Form,File,UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session 
from models.postmodel import updatePostModel as UPM 
from database.crud import create_post,get_all_post,edit_post,delete_post,get_a_post
from database.connect import get_db
from auth.oauth import get_blogger
from database.model import Blogger

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

@postRouter.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id:int,db:Session = Depends(get_db),current_blogger: Blogger = Depends(get_blogger)):
   return delete_post(post_id=id,db=db, current_blogger= current_blogger)

@postRouter.get("/read")
def get_all_route(db:Session = Depends(get_db)):
   return get_all_post(db = db)

@postRouter.get("/by-name/{name}")
def getpost(title:str,db:Session = Depends(get_db)):
    return get_a_post(title,db=db)