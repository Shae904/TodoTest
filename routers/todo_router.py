from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Literal, Optional

from database import get_db
from schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse
from services import todo_service


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.post("/", response_model=TodoResponse)
async def create_todo(task: str, person: str, db: Session = Depends(get_db)):
    todo_data = TodoCreate(task = task, person = person)
    return todo_service.create_todo(db, todo_data)

@router.get("/filter/", response_model=list[TodoResponse])
async def filter_todos(
    task: Optional[str] = None,
    person: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return todo_service.filter_todos(db, task, person)

@router.get("/sort/", response_model=list[TodoResponse])
async def sort_todos(
    sort_by: Literal["task","person"],
    db: Session = Depends(get_db)
):
    todos = todo_service.sort_todos(db, sort_by)

    if todos is None:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be either 'task' or 'person'"
        )

    return todos


@router.get("/{todoid}", response_model=TodoResponse)
async def read_todo(todoid: int, db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, todoid)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todoid}", response_model=TodoResponse)
async def update_todo(
    todoid: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db)
):
    todo = todo_service.update_todo(db, todoid, todo_data)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.delete("/{todoid}")
async def delete_todo(todoid: int, db: Session = Depends(get_db)):
    todo = todo_service.delete_todo(db, todoid)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}