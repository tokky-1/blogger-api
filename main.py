from fastapi import FastAPI
from routes import bloggerroutes,postroutes
from middleware import ratelimit
import os

app = FastAPI(title="BLOGGER API", description="has the basic functionality of a blog site and some")

port = int(os.environ.get("PORT",5001))

app.add_middleware(ratelimit)
app.include_router(bloggerroutes.bloggerRouter,tags =["Users"] )
app.include_router(postroutes.postRouter,tags=["Posts"])

