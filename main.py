from fastapi import FastAPI
from routes import bloggerroutes
app = FastAPI(title="BLOGGER API", description="has the basic functionality of a blog site and some")

app.include_router(bloggerroutes.bloggerRouter,tags =["Users"] )
