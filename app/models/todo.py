from sqlalchemy import String
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Todo(db.Model):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='todos') # type: ignore

    def __repr__(self) -> str:
        return f'<Todo {self.title}>'