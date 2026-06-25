from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    todoid: Mapped[int] = mapped_column(primary_key=True, index=True)
    task: Mapped[str] = mapped_column()
    person: Mapped[str] = mapped_column()