import pytest
import tempfile
import os

from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    class Config:
        TESTING = True
        SECRET_KEY = 'testkey'
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

    app = create_app(Config)

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(email='test@example.com', first_name='Test', last_name='User')
        user.password = generate_password_hash('password', method='pbkdf2:sha256')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user