from flask_login import current_user, login_required
from flask import flash, redirect, render_template, request, url_for

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
    return render_template('create_or_update_todo.html')

@bp.route('/<int:todo_id>/update')
@login_required
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        flash('Todo not found.', 'error')
        return redirect(url_for('todos.list_todos'))
    if not todo.user_id == current_user.id:
        flash('You are not authorized to update this todo.', 'error')
        return redirect(url_for('todos.list_todos'))
    return render_template('create_or_update_todo.html', todo=todo)

@bp.route('/create', methods=['POST'])
@bp.route('/<int:todo_id>/update', methods=['POST'])
@login_required
def create_or_update(todo_id=None):
    title = request.form.get('title')
    description = request.form.get('description')

    if todo_id:
        todo = db.session.query(Todo).filter(Todo.id==todo_id).first()
        if not todo:
            flash('Todo not found.', 'error')
            return redirect(url_for('todos.list_todos'))
        if not todo.user_id == current_user.id:
            flash('You are not authorized to update this todo.', 'error')
            return redirect(url_for('todos.list_todos'))
    else:
        todo = Todo(user_id=current_user.id)

    if not title or not description:
        flash('All fields are required.', 'error')
        return redirect(url_for('todos.create' if not todo_id else 'todos.update', todo_id=todo_id))

    todo.title = title
    todo.description = description
    db.session.add(todo)
    db.session.commit()

    flash('Todo saved.', 'success')
    return redirect(url_for('todos.list_todos'))


@bp.route('/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        flash('Todo not found.', 'error')
        return redirect(url_for('todos.list_todos'))

    if todo.user_id != current_user.id:
        flash('You are not authorized to delete this todo.', 'error')
        return redirect(url_for('todos.list_todos'))
    
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos.list_todos'))
