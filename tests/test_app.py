import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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
        # cleanup
        db.session.delete(task)
        db.session.commit()


def test_complete_task(client):
    with app.app_context():
        task = Task(title='Complete Me', category='Testing')
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f'/complete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed is True
        # cleanup
        db.session.delete(task)
        db.session.commit()


def test_delete_task(client):
    with app.app_context():
        task = Task(title='Delete Me', category='Testing')
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f'/delete/{task_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None