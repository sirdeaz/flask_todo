from curses import flash
from flask_login import current_user, login_required
from flask import redirect, render_template, request, url_for

from app.extensions import db
from app.todo import bp
from app.models.todo import Todo

@bp.route('/')
@login_required
def list_todos():
    todos = db.session.query(Todo).filter(Todo.user_id==current_user.id).all()
    return render_template('list_todos.html', todos=todos)
    

@bp.route('/create')
@login_required
def create():
    return render_template('create_todo.html')

@bp.route('/create', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title')
    description = request.form.get('description')

    if not title or not description:
        flash('All fields are required.', 'error')
        return redirect(url_for('todos.create'))
    
    todo = Todo(title=title, description=description, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos.list_todos'))


@bp.route('/<int:todo_id>/delete')
@login_required
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id==todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos.list_todos'))
