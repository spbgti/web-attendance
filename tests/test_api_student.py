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

    def test_create_student(self, db, test_client):
        resp = test_client.post('/students', data=json.dumps(dict(name='name', group_number='123')), content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {
            'status': 'Created',
            'student': {
                'group_number': '123',
                'id': 1,
                'name': 'name'
            }
        }
        assert resp.status_code == 201
        assert data == expected_data

    def test_create_student_invalid_json(self, db, test_client):
        resp = test_client.post('/students', data="invalid json",
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Invalid json'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_create_student_requires_name_value(self, db, test_client):
        resp = test_client.post('/students', data=json.dumps(dict(fio='name', group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Requires name and group_number values'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_create_student_requires_group_value(self, db, test_client):
        resp = test_client.post('/students', data=json.dumps(dict(name='name', text='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Requires name and group_number values'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_create_student_wrong_type_name(self, db, test_client):
        resp = test_client.post('/students', data=json.dumps(dict(name=123, group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'name must be str value'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_create_student_wrong_type_group(self, db, test_client):
        resp = test_client.post('/students', data=json.dumps(dict(name='name', group_number=123)),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'group_number must be str value'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_create_student_repeat_data(self, db, test_client):
        Student(name='name', group_number='123').save()
        resp = test_client.post('/students', data=json.dumps(dict(name='name', group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Found same student'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(name='name11', group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {
            'status': 'Edited',
            'student': {
                'group_number': '123',
                'id': 1,
                'name': 'name11'
            }
        }
        assert resp.status_code == 200
        assert data == expected_data

    def test_edit_student_invalid_json(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data='TEXT',
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Invalid json'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student_non_existent_student(self, db, test_client):
        resp = test_client.put('/students/1', data=json.dumps(dict(name='name11', group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Student not found'}
        assert resp.status_code == 404
        assert data == expected_data

    def test_edit_student_requires_name_value(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(TEXT='name11', group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Requires name and group_number values'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student_requires_group_value(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(name='name11', TEXT='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Requires name and group_number values'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student_wrong_name_type(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(name=11, group_number='123')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'name must be str value'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student_wrong_group_type(self, db, test_client):
        Student(name='name1', group_number='111').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(name='name11', group_number=123)),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'group_number must be str value'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_student_repeat_data(self, db, test_client):
        Student(name='name1', group_number='111').save()
        Student(name='name2', group_number='222').save()
        resp = test_client.put('/students/1', data=json.dumps(dict(name='name2', group_number='222')),
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Found the same student'}
        assert resp.status_code == 400
        assert data == expected_data
