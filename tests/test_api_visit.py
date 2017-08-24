from datetime import date

import pytest

from models import Student, Visit

BASE_URL = '/api/v1'


class TestBasicAPIVisit:
    """
        Содержит тесты для объектов с базовым API типа: /visit и /visit/<visit_id>
    """
    def test_get_visit_by_id(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.get(BASE_URL + '/visits/1')
        data = resp.json()
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

    def test_get_non_existent_visit(self, db, test_client):
        resp = test_client.get(BASE_URL + '/visits/1')
        data = resp.json()
        expected_data = {'status': 'Visit not found'}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_all_visit(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        student = Student(name='name2', group_number='222')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.get(BASE_URL + '/visits')
        data = resp.json()
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

    def test_create_visit(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        resp = test_client.post(
            BASE_URL + '/visits',
            json={
                'student_id': 1,
                'date': '2017.01.01',
                'pair_num': 1
            },
        )
        data = resp.json()
        expected_data = {
            'status': 'Created',
            "visit": {
                "date": "2017.01.01",
                "id": 1,
                "pair_num": 1,
                "student_id": 1
            }
        }
        assert resp.status_code == 201
        assert data == expected_data

    def test_create_visit_invalid_json(self, db, test_client):
        resp = test_client.post(
            BASE_URL + '/visits',
            data='Invalid json',
        )
        data = resp.json()
        expected_data = {'status': 'Invalid json'}
        assert resp.status_code == 400
        assert data == expected_data

    @pytest.mark.parametrize('data, expected_data, status_code', [
        ({'date': '2017.01.01', 'pair_num': 1}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': 1, 'pair_num': 1}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': 1, 'date': '2017.01.01'}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': '1', 'date': '2017.01.01', 'pair_num': 1}, {'status': 'student_id must be int value'}, 400),
        ({'student_id': 2, 'date': '2017.01.01', 'pair_num': 1}, {'status': 'Student not found'}, 404),
        ({'student_id': 1, 'date': '2017', 'pair_num': 1}, {'status': 'Invalid date format, try YYYY.MM.DD'}, 400),
        ({'student_id': 1, 'date': '2017.01.01', 'pair_num': '1'}, {'status': 'pair_num must be int value'}, 400),
        ({'student_id': 1, 'date': '2017.01.01', 'pair_num': 10}, {'status': 'pair_num must be from 1 to 4'}, 400),
    ])
    def test_create_visit_wrong_input(self, db, test_client, data, expected_data, status_code):
        student = Student(name='name', group_number='123')
        student.save()
        resp = test_client.post(
            BASE_URL + '/visits',
            json=data,
        )
        data = resp.json()
        assert resp.status_code == status_code
        assert data == expected_data

    def test_create_visit_repeat_data(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017,1,1), pair_num=1).save()
        resp = test_client.post(
            BASE_URL + '/visits',
            json={
                'student_id': 1,
                'date': '2017.01.01',
                'pair_num': 1
            },
        )
        data = resp.json()
        expected_data = {'status': 'Found the same visit'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_edit_visit(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.put(
            BASE_URL + '/visits/1',
            json={
                'student_id': 1,
                'date': '2017.03.01',
                'pair_num': 1
            },

        )
        data = resp.json()
        expected_data = {
            'status': 'Edited',
            "visit": {
                "date": "2017.03.01",
                "id": 1,
                "pair_num": 1,
                "student_id": 1
            }
        }
        assert resp.status_code == 200
        assert data == expected_data

    def test_edit_non_existent_visit(self, db, test_client):
        resp = test_client.put(
            BASE_URL + '/visits/1',
            json={
                'student_id': 1,
                'date': '2017.03.01',
                'pair_num': 1
            },
        )
        data = resp.json()
        expected_data = {'status': 'Visit not found'}
        assert resp.status_code == 404
        assert data == expected_data

    def test_edit_visit_invalid_json(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.put(
            BASE_URL + '/visits/1',
            data='TEXT',
        )
        data = resp.json()
        expected_data = {'status': 'Invalid json'}
        assert resp.status_code == 400
        assert data == expected_data

    @pytest.mark.parametrize('data, expected_data, status_code', [
        ({'date': '2017.03.01', 'pair_num': 1}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': 1, 'pair_num': 1}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': 1, 'date': '2017.03.01'}, {'status': 'Requires student_id, date and pair_num values'}, 400),
        ({'student_id': '1', 'date': '2017.03.01', 'pair_num': 1}, {'status': 'student_id must be int value'}, 400),
        ({'student_id': 2, 'date': '2017.03.01', 'pair_num': 1}, {'status': 'Student not found'}, 404),
        ({'student_id': 1, 'date': '2017', 'pair_num': 1}, {'status': 'Invalid date format, try YYYY.MM.DD'}, 400),
        ({'student_id': 1, 'date': '2017.03.01', 'pair_num': '1'}, {'status': 'pair_num must be int value'}, 400),
        ({'student_id': 1, 'date': '2017.03.01', 'pair_num': 10}, {'status': 'pair_num must be from 1 to 4'}, 400),
    ])
    def test_edit_visit_wrong_input(self, db, test_client, data, expected_data, status_code):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.put(
            BASE_URL + '/visits/1',
            json=data,
        )
        data = resp.json()
        assert resp.status_code == status_code
        assert data == expected_data

    def test_edit_visit_repeat_data(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 4), pair_num=2).save()
        resp = test_client.put(
            BASE_URL + '/visits/1',
            json={
                'student_id': 1,
                'date': '2017.01.04',
                'pair_num': 2
            },
        )
        data = resp.json()
        expected_data = {'status': 'Found the same visit'}
        assert resp.status_code == 400
        assert data == expected_data

    def test_delete_visit(self, db, test_client):
        student = Student(name='name', group_number='123')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        resp = test_client.delete(BASE_URL + '/visits/1')
        data = resp.json()
        expected_data = {'status': 'Visit is deleted'}
        assert resp.status_code == 200
        assert data == expected_data

    def test_delete_non_exsistnt_visit(self, db, test_client):
        resp = test_client.delete(BASE_URL + '/visits/1')
        data = resp.json()
        expected_data = {'status': 'Visit not found'}
        assert resp.status_code == 404
        assert data == expected_data


class TestExpandedAPIVisit:
    """
    Содержит тесты для объектов с API отличным от базового
    """
    def test_get_visit_by_day(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get(BASE_URL + '/visits/student/1/date/2017.01.01')
        data = resp.json()
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

    def test_get_visit_by_day_non_existent_student(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get(BASE_URL + '/visits/student/2/date/2017.01.01')
        data = resp.json()
        expected_data = {"status": "Student not found"}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_visit_by_day_invalid_date(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get(BASE_URL + '/visits/student/1/date/2017')
        data = resp.json()
        expected_data = {"status": "Invalid date format, try YYYY.MM.DD"}
        assert data == expected_data
        assert resp.status_code == 400

    def test_get_visit_by_week(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        Visit(student=student, date=date(2017, 1, 2), pair_num=4).save()
        Visit(student=student, date=date(2017, 1, 3), pair_num=3).save()
        resp = test_client.get(BASE_URL + '/visits/student/1/week/2017.01.01')
        data = resp.json()
        expected_data = {
            "status": "OK",
            "visits": {
                "pairs": {
                    "2017.01.01": {
                        "1": True,
                        "2": True,
                        "3": False,
                        "4": False
                    },
                    "2017.01.02": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": True
                    },
                    "2017.01.03": {
                        "1": False,
                        "2": False,
                        "3": True,
                        "4": False
                    },
                    "2017.01.04": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017.01.05": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017.01.06": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017.01.07": {
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

    def test_get_visit_by_week_non_existent_student(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get(BASE_URL + '/visits/student/2/week/2017.01.01')
        data = resp.json()
        expected_data = {"status": "Student not found"}
        assert data == expected_data
        assert resp.status_code == 404

    def test_get_visit_by_week_invalid_date(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        resp = test_client.get(BASE_URL + '/visits/student/1/week/2017')
        data = resp.json()
        expected_data = {"status": "Invalid date format, try YYYY.MM.DD"}
        assert data == expected_data
        assert resp.status_code == 400

    def test_get_visit_by_week_between(self, db, test_client):
        student = Student(name='name1', group_number='111')
        student.save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=1).save()
        Visit(student=student, date=date(2017, 1, 1), pair_num=2).save()
        Visit(student=student, date=date(2017, 1, 2), pair_num=4).save()
        Visit(student=student, date=date(2017, 1, 3), pair_num=3).save()
        resp = test_client.get(BASE_URL + '/visits/student/1/week/2016.12.30')
        data = resp.json()
        expected_data = {
            "status": "OK",
            "visits": {
                "pairs": {
                    "2016.12.30": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2016.12.31": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017.01.01": {
                        "1": True,
                        "2": True,
                        "3": False,
                        "4": False
                    },
                    "2017.01.02": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": True
                    },
                    "2017.01.03": {
                        "1": False,
                        "2": False,
                        "3": True,
                        "4": False
                    },
                    "2017.01.04": {
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False
                    },
                    "2017.01.05": {
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
