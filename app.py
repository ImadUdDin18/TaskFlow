import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

logging.basicConfig(
    filename='app_errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'change-this-secret-key-in-production'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access TaskFlow.'
login_manager.login_message_category = 'info'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='General')
    priority = db.Column(db.String(20), default='Medium')
    tags = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def run_auto_migration():
    """Auto-add any Task/User model columns missing from the actual DB tables.
    This fixes 'no such column' errors that happen when the model is updated
    (e.g. adding priority/tags/due_date) but the old tasks.db file still has
    the old table schema. Safe to run every time the app starts."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()

    for model in (User, Task):
        table_name = model.__tablename__
        if table_name not in existing_tables:
            continue  # brand new table, db.create_all() below will handle it

        existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
        model_columns = model.__table__.columns

        for column in model_columns:
            if column.name in existing_columns:
                continue

            col_type = column.type.compile(db.engine.dialect)
            default_clause = ''
            if column.default is not None and column.default.is_scalar:
                default_value = column.default.arg
                if isinstance(default_value, str):
                    default_clause = f" DEFAULT '{default_value}'"
                elif isinstance(default_value, bool):
                    default_clause = f" DEFAULT {int(default_value)}"
                elif default_value is not None:
                    default_clause = f" DEFAULT {default_value}"

            alter_sql = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}{default_clause}'
            with db.engine.connect() as conn:
                conn.execute(text(alter_sql))
                conn.commit()
            logging.info(f"Auto-migration: added missing column '{column.name}' to '{table_name}'")


with app.app_context():
    db.create_all()
    try:
        run_auto_migration()
    except Exception as e:
        logging.error(f"Auto-migration failed: {e}")


# ---------------- AUTH ROUTES ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            db.session.rollback()
            flash('Something went wrong. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        return redirect('/')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------------- TASK ROUTES (now user-scoped) ----------------

@app.route('/')
@login_required
def home():
    try:
        filter_type = request.args.get('filter', 'all')
        search_query = request.args.get('q', '').strip()

        query = Task.query.filter_by(user_id=current_user.id)

        if search_query:
            query = query.filter(Task.title.ilike(f'%{search_query}%'))

        if filter_type == 'pending':
            query = query.filter_by(completed=False)
        elif filter_type == 'completed':
            query = query.filter_by(completed=True)

        tasks = query.order_by(Task.created_at.desc()).all()

        all_tasks = Task.query.filter_by(user_id=current_user.id).all()
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
@login_required
def add_task():
    title = request.form.get('title', '').strip()
    category = request.form.get('category')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date') or None
    tags = request.form.get('tags', '').strip() or None

    if not title or len(title) > 200:
        return redirect('/')

    try:
        new_task = Task(
            title=title, category=category, priority=priority,
            due_date=due_date, tags=tags, user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        db.session.rollback()

    return redirect('/?added=1')


@app.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
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
@login_required
def complete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if task is None:
        return redirect('/')
    task.completed = not task.completed
    db.session.commit()
    return redirect('/?updated=1')


@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
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
@login_required
def stats():
    from collections import defaultdict

    try:
        week_data = defaultdict(int)

        completed_tasks = Task.query.filter_by(completed=True, user_id=current_user.id).all()
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