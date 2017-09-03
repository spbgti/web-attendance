import pytest

from models import Student

BASE_URL = '/auth/v1'


class TestAuthentication:
    """
    Содержит тесты для объектов /index, /login/<student_id>, /logout
    """
    def test_auth_non_existent_student(self, db, test_client):
        resp = test_client.get(BASE_URL + '/index')
        data = resp.json()
        expected_data = {'status': 'auth required'}
        assert resp.status_code == 401
        assert data == expected_data

    def test_login_student(self, db, test_client):
        Student(name='name', group_number='123').save()
        resp = test_client.get(BASE_URL + '/loading/1')
        # что возвращает редирект? если ссылку, то как на неё переходят?
        # resp = test_client.get(BASE_URL + '/index')
        data = resp.json()
        print(data)
        #expected_data = {'status': 'OK', 'information': 'name'}
        #assert resp.status_code == 200
        #assert data == expected_data
