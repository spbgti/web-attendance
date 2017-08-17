from datetime import date
import json
from models import Student, Visit
import pytest


@pytest.fixture
def test_client(app):
    return app.test_client()


class TestBasicAPIVisit:
    def test_get_by_id(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.get('/visits/1')
        data = json.loads(resp.data.decode())
        expected_data = {
            "status": "OK",
            "visit": {
                "date": "2017.01.01",
                "id": 1,
                "pair_num": 1,
                "student_id": 1
            }
        }

        assert resp.status_code == 200
        assert data == expected_data

    def test_get_null_visit(self, db, test_client):
        resp = test_client.get('/visits/1')
        data = json.loads(resp.data.decode())
        expected_data = {'status': 'Visit not found'}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_all_visits(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        student = Student(name='name2', group_number='222')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.get('/visits')
        data = json.loads(resp.data.decode())
        expected_data = {
            "status": "OK",
            "visits": [
                {"date": "2017.01.01", "id": 1, "pair_num": 1, "student_id": 1},
                {"date": "2017.01.01", "id": 2, "pair_num": 2, "student_id": 1},
                {"date": "2017.01.01", "id": 3, "pair_num": 1, "student_id": 2}
            ]
        }
        assert data == expected_data
        assert resp.status_code == 200

    def test_get_day(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get('/visits/student/1/date/2017.01.01')
        data = json.loads(resp.data.decode())
        expected_data = {
            "status": "OK",
            "visits": {
                "date": "2017.01.01",
                "pairs": {
                    "1": True,
                    "2": True,
                    "3": False,
                    "4": False
                },
                "student": 1
            }
        }
        assert data == expected_data
        assert resp.status_code == 200

    def test_get_day_null_student(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get('/visits/student/2/date/2017.01.01')
        data = json.loads(resp.data.decode())
        expected_data = {"status": "Student not found"}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_day_null_data(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get('/visits/student/1/date/2017')
        data = json.loads(resp.data.decode())
        expected_data = {"status": "Invalid date format, try YYYY.MM.DD"}
        assert data == expected_data
        assert resp.status_code == 400

    def test_get_week(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        Visit(student=student, date=date(2017, 1, 2), pair_num=4).save()
        Visit(student=student, date=date(2017, 1, 3), pair_num=3).save()
        resp = test_client.get('/visits/student/1/week/2017.01.01')
        data = json.loads(resp.data.decode())
        expected_data = {
            "status": "OK",
            "visits": {
                "pairs": {
                    "2017-01-01": {
                        "1": True,
                        "2": True,
                        "3": False,
                        "4": False
                    },
                    "2017-01-02": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": True
                    },
                    "2017-01-03": {
                        "1": False,
                        "2": False,
                        "3": True,
                        "4": False
                    },
                    "2017-01-04": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017-01-05": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017-01-06": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017-01-07": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    }
                },
                "student": 1
            }
        }
        assert data == expected_data
        assert resp.status_code == 200

    def test_get_week_null_student(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get('/visits/student/2/week/2017.01.01')
        data = json.loads(resp.data.decode())
        expected_data = {"status": "Student not found"}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_week_null_data(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get('/visits/student/1/week/2017')
        data = json.loads(resp.data.decode())
        expected_data = {"status": "Invalid date format, try YYYY.MM.DD"}
        assert data == expected_data
        assert resp.status_code == 400
