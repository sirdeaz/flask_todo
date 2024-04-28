from flask import url_for
from app.models.todo import Todo
from app.extensions import db

def test_list_todos_succeeds_if_logged_in(client, auth, user):
    auth.login(user.email, 'password')
    response = client.get('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert b'My Todos' in response.data

def test_list_todos_fails_if_not_logged_in(client):
    response = client.get('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_create_todo_succeeds_if_logged_in(client, auth, user):
    auth.login(user.email, 'password')
    response = client.post('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert b'create todo' in response.data

def test_create_todo_fails_if_not_logged_in(client, user):
    response = client.post('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_list_todos_returns_template_and_todos_when_logged_in_and_has_todos(client, app, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=user)
        todo2 = Todo(title='Test Todo2', description='Test Description2', user=user)
        db.session.add_all([todo1, todo2])
        db.session.commit()

    response = client.get('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert b'My Todos' in response.data
    assert b'Test Todo1' in response.data
    assert b'Test Todo2' in response.data
