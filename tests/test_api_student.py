import json
from models import Student
import pytest


@pytest.fixture
def test_client(app):
    return app.test_client()

class TestBasicAPIStudent:
    def test_get_by_id(self, db, test_client):
        Student(name='name', group_number='123').save()
        resp = test_client.get('/students/1')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'OK', 'student': {
            'id': 1, 'name': 'name', 'group_number': '123'
        }}
        assert resp.status_code == 200
        assert data == expected_data

    def test_get_nonexist_student(self, db, test_client):
        resp = test_client.get('/students/1')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Student not found'}
        assert data == expected_data
        assert resp.status_code == 404

