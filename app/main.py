from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, authentication, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(authentication.router)


@app.get("/")  # Define a path/route operation.
async def root():  # async is optional. Used to async operations.
    return {"message": "Hello World"}  # FastAPI auto converts to JSON
