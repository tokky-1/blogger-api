from pydantic import BaseModel,Field
from fastapi import File,UploadFile
from typing import Optional
from datetime import datetime

class postModel(BaseModel): # when using model object is always a dictionary
    title :str = Field(description="post title",example="My First Blog Post") 
    content: str = Field(description="post content")
    uploads:  Optional[list[UploadFile]] = File()
    acct_id: int

class updatePostModel(BaseModel): # when using model object is always a dictionary
    title : Optional[str] = Field(description="post title",example="My First Blog Post") 
    content: Optional[str] = Field(description="post content")
