from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='General')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    total = len(tasks)
    completed = len([t for t in tasks if t.completed])
    pending = total - completed
    return render_template('index.html', tasks=tasks, total=total, completed=completed, pending=pending)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    category = request.form.get('category')
    if title:
        new_task = Task(title=title, category=category)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)