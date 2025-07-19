from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class bloggerModel(BaseModel): # when using model object is always a dictionary
    username :str = Field(description="User name") 
    email: EmailStr = Field(description="User EMail")

class createBloggertModel(bloggerModel):
    fullname:  str = Field(description=" User's fullname")
    password : str = Field(default="password",description="password of the User")

class updateBloggerModel(BaseModel):
    username : Optional[str] = Field(None,description="User name ") 
    fullname:  Optional[str] = Field(None,description=" User's fullname")
    password :  Optional[str] = Field(default="password",description="password of the User")
