from fastapi import FastAPI

from database import Base, engine
from routers.todo_router import router as todo_router
import models


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo_router)