from sqlalchemy import Column,String,Integer,LargeBinary,ForeignKey,DateTime,func,Text
from .connect import engine
from sqlalchemy.ext.declarative import declarative_base 

base = declarative_base()

class Blogger(base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True,nullable=False)
    fullname = Column(String)
    username = Column(String)
    email = Column(String,)
    password = Column(String)

class Post(base):
    __tablename__ = "posts"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True,nullable=False)
    title = Column(String)
    content = Column(Text)
    uploads = Column(LargeBinary,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer,ForeignKey("users.id"))

base.metadata.create_all(bind=engine) 