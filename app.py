import logging
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

logging.basicConfig(
    filename='app_errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='General')
    priority = db.Column(db.String(20), default='Medium')
    tags = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    try:
        filter_type = request.args.get('filter', 'all')
        search_query = request.args.get('q', '').strip()

        query = Task.query

        if search_query:
            query = query.filter(Task.title.ilike(f'%{search_query}%'))

        if filter_type == 'pending':
            query = query.filter_by(completed=False)
        elif filter_type == 'completed':
            query = query.filter_by(completed=True)

        tasks = query.order_by(Task.created_at.desc()).all()

        all_tasks = Task.query.all()
        total = len(all_tasks)
        completed = len([t for t in all_tasks if t.completed])
        pending = total - completed

        return render_template(
            'index.html',
            tasks=tasks, total=total, completed=completed, pending=pending,
            current_filter=filter_type, search_query=search_query,
            today=datetime.utcnow().strftime('%Y-%m-%d')
        )
    except Exception as e:
        logging.error(f"Error loading home page: {e}")
        return render_template('500.html'), 500

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    category = request.form.get('category')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date') or None
    tags = request.form.get('tags', '').strip() or None

    if not title or len(title) > 200:
        return redirect('/')

    try:
        new_task = Task(title=title, category=category, priority=priority, due_date=due_date, tags=tags)
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        db.session.rollback()

    return redirect('/?added=1')

@app.route('/edit/<int:id>', methods=['POST'])
def edit_task(id):
    task = Task.query.get(id)
    new_title = request.form.get('title', '').strip()

    if task is None or not new_title or len(new_title) > 200:
        return redirect('/')

    try:
        task.title = new_title
        db.session.commit()
    except Exception as e:
        logging.error(f"Error editing task: {e}")
        db.session.rollback()

    return redirect('/?updated=1')

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    if task is None:
        return redirect('/')
    task.completed = not task.completed
    db.session.commit()
    return redirect('/?updated=1')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/?deleted=1')

@app.route('/health')
def health_check():
    try:
        Task.query.first()
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 503

@app.route('/stats')
def stats():
    from collections import defaultdict

    try:
        week_data = defaultdict(int)

        completed_tasks = Task.query.filter_by(completed=True).all()
        for t in completed_tasks:
            day_name = t.created_at.strftime('%a')
            week_data[day_name] += 1

        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        labels = days_order
        values = [week_data.get(day, 0) for day in days_order]

        return {'labels': labels, 'values': values}
    except Exception as e:
        logging.error(f"Error loading stats: {e}")
        return {'labels': [], 'values': []}, 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    logging.error(f"Server Error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)