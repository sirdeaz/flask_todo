from flask import url_for
import pytest
from app.models.todo import Todo
from app.extensions import db
from app.models.user import User

def test_list_todos_succeeds_if_logged_in(client, auth, user):
    auth.login(user.email, 'password')
    response = client.get('/todos', follow_redirects=True)
    assert response.status_code == 200
    assert b'My Todos' in response.data

def test_list_todos_fails_if_not_logged_in(client):
    response = client.get('/todos/create', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_create_todo_succeeds_if_logged_in(client, auth, user):
    auth.login(user.email, 'password')
    response = client.post('/todos/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'Create Todo' in response.data

def test_create_todo_fails_if_not_logged_in(client, user):
    response = client.post('/todos/create', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

@pytest.mark.parametrize(('title', 'description', 'message'), (
    ('', '', b'All fields are required.'),
    ('a', '',b'All fields are required.'),
    ('', 'a',b'All fields are required.'),))
def test_create_todo_field_validation(client, auth, user, title, description, message):
    auth.login(user.email, 'password')
    response = client.post('/todos/create', data={'title': title, 'description': description}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data

def test_create_todo_creates_new_todo(client, auth, user):
    auth.login(user.email, 'password')
    response = client.post('/todos/create', data={'title': 'Test Todo', 'description': 'Test Description'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Todo' in response.data


def test_update_todo_get_fails_if_not_logged_in(client, user):
    response = client.get('/todos/update/1', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_update_todo_get_fails_if_todo_does_not_exist(client, auth, user):
    auth.login(user.email, 'password')
    response = client.get('/todos/update/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Todo not found' in response.data

def test_update_todo_get_fails_if_user_is_not_owner(app, client, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        other_user = User(email='test@example2.com', first_name='Test', last_name='User', password='password')
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=other_user)
        db.session.add(todo1)
        db.session.commit()
        response = client.get(f'/todos/update/{todo1.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'You are not authorized to update this todo' in response.data

def test_update_todo_get_returns_template_and_todo_when_logged_in_and_has_todo(app, client, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=user)
        db.session.add(todo1)
        db.session.commit()
        response = client.get(f'/todos/update/{todo1.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Todo1' in response.data
        assert b'Test Description1' in response.data

def test_update_todo_post_updates_title_and_description(app, client, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=user)
        db.session.add(todo1)
        db.session.commit()

        response = client.post(f'/todos/update/{todo1.id}', data={'title': 'Updated Title', 'description': 'Updated Description'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Updated Title' in response.data
        assert b'Updated Description' in response.data

def test_update_todo_post_fails_if_todo_does_not_exist(app, client, auth, user):
    auth.login(user.email, 'password')
    response = client.post('/todos/update/1', data={'title': 'Updated Title', 'description': 'Updated Description'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Todo not found' in response.data

def test_update_todo_post_fails_if_user_is_not_owner(app, client, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        other_user = User(email='test@example2.com', first_name='Test', last_name='User', password='password')
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=other_user)
        db.session.add(todo1)
        db.session.commit()
        
        response = client.post(f'/todos/update/{todo1.id}/', data={'title': 'Updated Title', 'description': 'Updated Description'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'You are not authorized to update this todo' in response.data

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

def test_delete_todo_succeeds_if_logged_in(app, client, auth, user):
    auth.login(user.email, 'password')
    
    with app.app_context():
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=user)
        db.session.add(todo1)
        db.session.commit()
        response = client.post(f'/todos/delete/{todo1.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Todo1' not in response.data

def test_delete_todo_fails_if_not_logged_in(client, user):
    response = client.post('/todos/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_delete_if_todo_does_not_exist(app, client, auth, user):
    auth.login(user.email, 'password')
    response = client.post('/todos/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Todo not found' in response.data

def test_delete_if_user_is_not_owner(app, client, auth, user):
    auth.login(user.email, 'password')
    with app.app_context():
        other_user = User(email='test@example2.com', first_name='Test', last_name='User', password='password')
        todo1 = Todo(title='Test Todo1', description='Test Description1', user=other_user)
        db.session.add(todo1)
        db.session.commit()
        
        response = client.post(f'/todos/delete/{todo1.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'You are not authorized to delete this todo' in response.data

