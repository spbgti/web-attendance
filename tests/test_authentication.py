import pytest
from flask_login import current_user, login_user

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

    def test_auth_student(self, db, test_client, app):
        Student(name='name', group_number='123').save()
        student = Student.query.get(1)
        with app.test_request_context():
            with test_client as c:
                assert current_user.is_authenticated is False
                login_user(student)
                resp = c.get(BASE_URL + '/index')
                data = resp.json()
                expected_data = {'status': 'OK', 'information': 'name'}
                assert resp.status_code == 200
                assert data == expected_data

    def test_login_student(self, db, test_client, app):
        Student(name='name', group_number='123').save()
        with app.test_request_context():
            with test_client as c:
                assert current_user.is_authenticated is False
                r = c.get(BASE_URL + '/login/1')
                assert current_user.is_authenticated is True
                assert current_user.id == 1

    def test_logout_student(self, db, test_client, app):
        Student(name='name', group_number='123').save()
        student = Student.query.get(1)
        with app.test_request_context():
            with test_client as c:
                assert current_user.is_authenticated is False
                login_user(student)
                assert current_user.is_authenticated is True
                assert current_user.id == 1
                r = c.get(BASE_URL + '/logout')
                assert current_user.is_authenticated is False
