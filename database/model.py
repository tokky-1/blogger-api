from sqlalchemy import Column,String,Integer,LargeBinary,ForeignKey,DateTime,func,Text
from .connect import engine
from sqlalchemy.ext.declarative import declarative_base 

base = declarative_base()

class Blogger(base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    fullname = Column(String)
    username = Column(String,unique=True )
    email = Column(String,unique=True)
    password = Column(String)

class Post(base):
    __tablename__ = "posts"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)
    uploads = Column(LargeBinary,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer,ForeignKey("users.id") ,index=True)

base.metadata.create_all(bind=engine) 