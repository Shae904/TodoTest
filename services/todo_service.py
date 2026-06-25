from sqlalchemy.orm import Session
from models import Todo
from schemas.todo_schema import TodoCreate, TodoUpdate


def create_todo(db: Session, todo_data: TodoCreate):
    todo = Todo(
        task=todo_data.task,
        person=todo_data.person
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def get_todo(db: Session, todoid: int):
    return db.query(Todo).filter(Todo.todoid == todoid).first()


def update_todo(db: Session, todoid: int, todo_data: TodoUpdate):
    todo = db.query(Todo).filter(Todo.todoid == todoid).first()

    if todo is None:
        return None

    if todo_data.task is not None:
        todo.task = todo_data.task

    if todo_data.person is not None:
        todo.person = todo_data.person

    db.commit()
    db.refresh(todo)

    return todo


def delete_todo(db: Session, todoid: int):
    todo = db.query(Todo).filter(Todo.todoid == todoid).first()

    if todo is None:
        return None

    db.delete(todo)
    db.commit()

    return todo