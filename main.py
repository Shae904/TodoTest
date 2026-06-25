from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql+psycopg://postgres:" + os.getenv('DB_PASS') + "@localhost:5432/todoDB"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todos"
    todoid: Mapped[int] = mapped_column(primary_key=True, index=True)
    task: Mapped[str] = mapped_column()
    person: Mapped[str] = mapped_column()

Base.metadata.create_all(bind=engine)

app = FastAPI()     

@app.post("/todos/")
async def create_todo(task: str, person: str):
    db = SessionLocal()
    todo = Todo(task=task, person=person)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/")
async def read_todo(todoid: int):
    db = SessionLocal()
    return db.query(Todo).filter(Todo.todoid == todoid).first()

@app.put("/todos/{todoid}")
async def update_todo(todoid: int, task: str, person: str):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.todoid == todoid).first()
    todo.task = task
    todo.person = person
    db.commit()
    return todo

@app.delete("/todos/{todoid}")
async def delete_todo(todoid:int):
    db = SessionLocal()
    db.delete(db.query(Todo).filter(Todo.todoid == todoid).first())
    db.commit()
    return {"message": "Todo deleted successfully"}