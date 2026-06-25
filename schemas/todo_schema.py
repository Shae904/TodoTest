from pydantic import BaseModel


class TodoCreate(BaseModel):
    task: str
    person: str


class TodoUpdate(BaseModel):
    task: Optional[str] = None
    person: Optional[str] = None


class TodoResponse(BaseModel):
    todoid: int
    task: str
    person: str

    model_config = {
        "from_attributes": True
    }