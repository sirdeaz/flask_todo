from flask import Blueprint

bp = Blueprint('todos', __name__)

from app.todo import routes