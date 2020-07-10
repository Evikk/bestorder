from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    done = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    priority = db.Column(db.Integer)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    tasks = db.relationship('Task', backref='list')

@app.route('/newlist')
def new_list():
    list_options = List.query.all()
    return render_template ('newlist.html', list_options=list_options)

@app.route('/<list_id>/newtask')
def new_task(list_id):
    print(list_id)
    list_options = List.query.all()
    list = List.query.filter_by(id = list_id).first()
    return render_template ('newtask.html', list_options=list_options, list=list)

@app.route('/show', methods=['POST'])
@app.route('/')
def show_all():

    view = 'priority'
    view_select = request.form.get('view')
    if view_select == 'complete':
        view = 'complete'

    list_options = List.query.all()
    select = request.form.get('list_select')
    if select == 'All Lists':
        lists = List.query.all()
    else:
        lists = List.query.filter(List.id == select)
    tasks = List.query.filter(List.tasks).all()
    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options, list_select=select, view=view)

@app.route('/addlist', methods=['POST'])
def add_list():
    list = List(name=request.form['name'], description=request.form['description'])
    db.session.add(list)
    db.session.commit()
    lists = List.query.filter_by(name=request.form['name'])
    tasks = List.query.filter(List.tasks).all()
    list_options = List.query.all()
    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options)

@app.route('/<list_id>/deletelist', methods=['POST'])
def delete_list(list_id):
    
    tasks = List.query.filter(List.tasks).all()
    lists = List.query.all()
    list_options = List.query.all()
    list = List.query.filter(List.id == list_id).first()
    db.session.delete(list)
    db.session.commit()

    return render_template ('base.html', lists=lists, tasks=tasks, list_options=list_options)

@app.route('/<list_id>/addtask', methods=['POST'])
def add_task(list_id):
    
    list_options = List.query.all()
    lists = List.query.filter(List.id == list_id).all()
    tasks = List.query.filter(List.tasks).all()
    task = Task(description=request.form['description'], done=False, list_id=list_id, priority=request.form['priority'])
    db.session.add(task)
    db.session.commit()
    
    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options)


@app.route('/<list_id>/<task_id>/completetask', methods=['POST'])
def complete_task(list_id, task_id):

    task = Task.query.get(task_id)
    list_options = List.query.all()
    lists = List.query.filter(List.id == list_id).all()
    tasks = List.query.filter(List.tasks).all()

    if task.done:
        task.done = False
    else:
        task.done = True
    
    db.session.commit()

    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options)
    

@app.route('/<list_id>/<task_id>/deletetask', methods=['POST'])
def delete_task(list_id, task_id):

    list_options = List.query.all()
    lists = List.query.filter(List.id == list_id).all()
    tasks = List.query.filter(List.tasks).all()
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()

    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options)

@app.route('/<list_id>/<task_id>/edittask', methods=['POST'])
def edit_task(list_id, task_id):

    task = Task.query.filter_by(id = task_id).first()
    list_options = List.query.all()
    list = List.query.filter_by(id = list_id).first()
    

    return render_template ('edittask.html', list_options=list_options, list=list, task=task)

@app.route('/<list_id>/<task_id>/updatetask', methods=['POST'])
def task_update(list_id, task_id):

    list_options = List.query.all()
    lists = List.query.filter(List.id == list_id).all()
    tasks = List.query.filter(List.tasks).all()

    update = Task.query.filter_by(id = task_id).first()
    update.name = request.form['name']
    update.description = request.form['description']
    update.priority = request.form['priority']

    db.session.commit()

    return render_template ('tasks.html', lists=lists, tasks=tasks, list_options=list_options)

if __name__ == '__main__':
    app.run(debug=True)
