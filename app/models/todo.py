from sqlalchemy import String
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class todo(db.Model):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    user: Mapped['User'] = db.relationship('User', backref='todos')