import pytest
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from app.models.user import User
from app.extensions import db

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_post_succeed(client, user):
    response = client.post('/auth/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/profile'

def test_login_post_fail(client, user):
    response = client.post('/auth/login', data={'email': user.email, 'password': 'wrongpassword'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'All fields are required.'),
    ('a', '', b'All fields are required.'),
    ('', 'a', b'All fields are required.'),
))
def test_login_validate_input(client, email, password, message):

    response = client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)
    
    assert message in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_signup_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_signup_post(app, client):
    response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'
    with app.app_context():
        user = db.session.query(User).filter_by(email='test@example.com').first()
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert check_password_hash(user.password, 'password')

@pytest.mark.parametrize(('email', 'first_name', 'last_name', 'password', 'message'), (
    ('', '', '', '', b'All fields are required.'),
    ('a', '', '', '', b'All fields are required.'),
    ('', 'a', '', '', b'All fields are required.'),
    ('', '', 'a', '', b'All fields are required.'),
    ('', '', '', 'a', b'All fields are required.')
))
def test_signup_email_required(client, email, first_name, last_name, password, message):
    response = client.post('/auth/signup', data={'email': email, 
                                                 'first_name': first_name, 
                                                 'last_name': last_name, 
                                                 'password': password}, 
                                                 follow_redirects=True)
    assert message in response.data
    assert response.status_code == 200
    assert response.request.path == '/auth/signup'

def test_signup_email_unique(app, client):
    with app.app_context():
        user = User(email='test@example.com', first_name='Test', last_name='User', password='password')
        db.session.add(user)
        db.session.commit()
        response = client.post('/auth/signup', data={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
        assert b'Email already exists.' in response.data
        assert response.status_code == 200
        assert response.request.path == '/auth/signup'

def test_logout_get_fails(client):
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/auth/login'

def test_logout_get_succeeds(app, client, user):
    with app.app_context():
        response = client.post('/auth/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'