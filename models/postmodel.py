from pydantic import BaseModel,Field
from fastapi import File,UploadFile
from typing import Optional

class postModel(BaseModel): # when using model object is always a dictionary
    title :str = Field(description="User name") 
    content: str = Field(description="User EMail")
    uploads:  Optional[list[UploadFile]] = File()
  
