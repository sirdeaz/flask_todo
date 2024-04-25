from app.models.todo import Todo
from app.extensions import db
from app.models.user import User

def test_todo_model(app, user):
    with app.app_context():
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=user)
        todo2 = Todo(title='Test Todo2', description='Test Description2', user=user)

        db.session.add_all([todo1, todo2])
        db.session.commit()

        todos = db.session.query(Todo).all()
        assert len(todos) == 2
        assert todos[0].title == 'Test Todo1'
        assert todos[0].description == 'Test Description1'
        assert todos[0].user == user
        assert todos[1].title == 'Test Todo2'
        assert todos[1].description == 'Test Description2'
        assert todos[1].user == user

        user = db.session.query(User).first()
        assert len(user.todos) == 2
        