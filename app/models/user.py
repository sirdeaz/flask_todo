from flask_login import UserMixin
from sqlalchemy import String
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.first_name} {self.last_name}>'

