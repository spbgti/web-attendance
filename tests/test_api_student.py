import json
from models import Student
import pytest


@pytest.fixture
def test_client(app):
    return app.test_client()


class TestBasicAPIStudent:
    def test_get_student_by_id(self, db, test_client):
        Student(name='name', group_number='123').save()
        resp = test_client.get('/students/1')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'OK', 'student': {
            'id': 1, 'name': 'name', 'group_number': '123'
        }}
        assert resp.status_code == 200
        assert data == expected_data

    def test_get_non_existent_student(self, db, test_client):
        resp = test_client.get('/students/1')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Student not found'}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_all_student(self, db, test_client):
        Student(name='name1', group_number='123').save()
        Student(name='name2', group_number='124').save()
        Student(name='name3', group_number='123').save()
        resp = test_client.get('/students')
        data = json.loads(resp.data.decode())
        expected_data = {
            'status': 'OK',
            'students': [
                {'group_number': '123', 'id': 1, 'name': 'name1'},
                {'group_number': '124', 'id': 2, 'name': 'name2'},
                {'group_number': '123', 'id': 3, 'name': 'name3'}
            ]
        }
        assert data == expected_data
        assert resp.status_code == 200

    def test_get_group(self, db, test_client):
        Student(name='name1', group_number='123').save()
        Student(name='name2', group_number='124').save()
        Student(name='name3', group_number='123').save()
        Student(name='name4', group_number='123M').save()
        resp = test_client.get('/students/group/123')
        data = json.loads(resp.data.decode())
        expected_data = {
            'status': 'OK',
            'students': [
                {'group_number': '123', 'id': 1, 'name': 'name1'},
                {'group_number': '123', 'id': 3, 'name': 'name3'}
            ]
        }
        assert data == expected_data
        assert resp.status_code == 200

    def test_get_non_existent_group(self, db, test_client):
        resp = test_client.get('/students/group/111')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Group not found'}
        assert data == expected_data
        assert resp.status_code == 404
