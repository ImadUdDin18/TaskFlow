import pytest
from app import app, db, Task, User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            existing = User.query.filter_by(username='pytest_user').first()
            if existing:
                Task.query.filter_by(user_id=existing.id).delete()
                db.session.delete(existing)
                db.session.commit()

        client.post('/register', data={
            'username': 'pytest_user',
            'email': 'pytest_user@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)

        client.post('/login', data={
            'username': 'pytest_user',
            'password': 'testpass123'
        }, follow_redirects=True)

        yield client

        with app.app_context():
            user = User.query.filter_by(username='pytest_user').first()
            if user:
                Task.query.filter_by(user_id=user.id).delete()
                db.session.delete(user)
                db.session.commit()


def get_test_user_id():
    with app.app_context():
        user = User.query.filter_by(username='pytest_user').first()
        return user.id


def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_task(client):
    response = client.post('/add', data={'title': 'Pytest Task', 'category': 'Testing'}, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = Task.query.filter_by(title='Pytest Task').first()
        assert task is not None
        assert task.category == 'Testing'
        db.session.delete(task)
        db.session.commit()


def test_complete_task(client):
    user_id = get_test_user_id()
    with app.app_context():
        task = Task(title='Complete Me', category='Testing', user_id=user_id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f'/complete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.completed is True
        db.session.delete(task)
        db.session.commit()


def test_delete_task(client):
    user_id = get_test_user_id()
    with app.app_context():
        task = Task(title='Delete Me', category='Testing', user_id=user_id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f'/delete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task is None