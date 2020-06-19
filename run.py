from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todotest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    done = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)


@app.route('/')
def show_all():
    lists = List.query.all()
    tasks = Task.query.all()
    return render_template ('main.html', tasks=tasks, lists=lists)

@app.route('/addlist', methods=['POST'])
def add_list():
    list = List(name=request.form['name'], description=request.form['description'])
    db.session.add(list)
    db.session.commit()

    return redirect('/')

@app.route('/<list_id>/add', methods=['POST'])
def add_task(list_id):
	task = Task(name=request.form['name'], description=request.form['description'], done=False, list_id=list_id)
	db.session.add(task)
	db.session.commit()

	return redirect('/')


@app.route('/done/<list_id>/<task_id>')
def complete(task_id, list_id):

    task = Task.query.get(task_id)
    list = List.query.get(list_id)
    task.done = True
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
