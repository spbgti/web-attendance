from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
from flask import Flask, jsonify, make_response, request
from models import db, Student, Visit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db.init_app(app)


# ---------------VISIT---------------

# ---GET---


@app.route('/visits/<int:visit_id>', methods=['GET'])
def get_visit_by_id(visit_id):
    visit = Visit.query.get(visit_id)

    if visit is None:
        return make_response(
            jsonify(status="Visit not found"),
            404)

    return make_response(
        jsonify(
            status='OK',
            visit=visit.to_dict()
        ),
        200
    )


@app.route('/visits', methods=['GET'])
def get_all_visits():
    visits = Visit.query.all()

    return make_response(
        jsonify(
            status='OK',
            visits=[visit.to_dict() for visit in visits]
        ),
        200
    )


@app.route('/visits/student/<int:student_id>/date/<pair_date>', methods=['GET'])
def get_visits_day(student_id, pair_date):
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:  # ловим исключение, и прописываем действие
        return make_response(
            jsonify(status='Invalid date format, try YYYY.MM.DD'),
            400
        )

    visits_by_day = Visit.query.filter_by(student=student, date=pair_date).all()

    pair_visits = {1: False, 2: False, 3: False, 4: False}

    for visit in visits_by_day:
        pair_visits[visit.pair_num] = True

    return make_response(
        jsonify(
            status='OK',
            visits={
                'student': student_id,
                'date': pair_date.strftime('%Y.%m.%d'),
                'pairs': pair_visits
            }
        ),
        200
    )


@app.route('/visits/student/<int:student_id>/week/<week_start>', methods=['GET'])
def get_visits_week(student_id, week_start):
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    try:
        week_start = datetime.strptime(week_start, '%Y.%m.%d').date()
    except ValueError:  # ловим исключение, и прописываем действие
        return make_response(
            jsonify(status='Invalid date format, try YYYY.MM.DD'),
            400
        )

    visits_by_week = {}

    for i in range(7):
        visits_by_day = Visit.query.filter_by(student=student, date=week_start).all()

        pair_visits = {1: False, 2: False, 3: False, 4: False}

        for visit in visits_by_day:
            pair_visits[visit.pair_num] = True

        # заполняем день
        visits_by_week[str(week_start)] = pair_visits
        week_start += timedelta(days=1)

    return make_response(
        jsonify(
            status='OK',
            visits={
                'student': student_id,
                'pairs': visits_by_week
            }
        ),
        200
    )


# ---POST---


@app.route('/visits', methods=['POST'])
def create_visit():
    visit_data = request.get_json(silent=True)

    if visit_data is None:
        return make_response(
            jsonify(status="Invalid json"),
            400
        )

    try:
        student_id = visit_data['student_id']
        pair_date = visit_data['date']
        pair_num = visit_data['pair_num']
    except KeyError:
        return make_response(
            jsonify(status="Requires student_id, date and pair_num values"),
            400
        )

    # студент
    if not isinstance(student_id, int):  # проверяем что student_id - int
        return make_response(
            jsonify(status="student_id must be int value"),
            400
        )

    student = Student.query.get(student_id)
    if student is None:
        return make_response(
            jsonify(status="Student not found"),
            400
        )

    # дата
    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:
        return make_response(
            jsonify(status="Invalid date format, try YYYY.MM.DD"),
            400
        )

    # номер пары
    if not isinstance(pair_num, int):
        return make_response(
            jsonify(status="pair_num must be int value"),
            400
        )

    if not 1 <= pair_num <= 4:
        return make_response(
            jsonify(status="pair_num must be from 1 to 4"),
            400
        )

    visit = Visit(date=pair_date, pair_num=pair_num, student=student)
    try:
        db.session.add(visit)
        db.session.commit()
        status_code = 201
        status = "Created"
    except IntegrityError:
        return make_response(
            jsonify(status='Found the same visit'),
            400
        )

    return make_response(
        jsonify(
            status=status,
            visit=visit.to_dict()
        ),
        status_code
    )


# ---PUT---


@app.route('/visits/<int:visit_id>', methods=['PUT'])
def edit_visit(visit_id):
    visit = Visit.query.get(visit_id)

    if visit is None:
        return make_response(jsonify(status="Visit not found"), 404)

    # извлекаем данные
    visit_data = request.get_json(silent=True)

    if visit_data is None:
        return make_response(
            jsonify(status="Invalid json"),
            400
        )

    try:
        student_id = visit_data['student_id']
        pair_date = visit_data['date']
        pair_num = visit_data['pair_num']
    except KeyError:
        return make_response(
            jsonify(status="Requires student_id, date and pair_num values"),
            400
        )

    # студент
    if not isinstance(student_id, int):  # проверяем что student_id - int
        return make_response(
            jsonify(status="student_id must be int value"),
            400
        )

    student = Student.query.get(student_id)
    if student is None:
        return make_response(
            jsonify(status="Student not found"),
            400
        )

    # дата
    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:
        return make_response(
            jsonify(status="Invalid date format, try YYYY.MM.DD"),
            400
        )

    # номер пары
    if not isinstance(pair_num, int):
        return make_response(
            jsonify(status="pair_num must be int value"),
            400
        )

    if not 1 <= pair_num <= 4:
        return make_response(
            jsonify(status="pair_num must be from 1 to 4"),
            400
        )

    try:
        visit.student_id = student_id
        visit.date = pair_date
        visit.pair_num = pair_num
        db.session.commit()
        status_code = 200
        status = "Edited"
    except IntegrityError:
        return make_response(
            jsonify(status='Found the same visit'),
            400
        )

    return make_response(
        jsonify(
            status=status,
            visit=visit.to_dict()
        ),
        status_code
    )


# ---DELETE---


@app.route('/visits/<int:visit_id>', methods=['DELETE'])
def delete_visit(visit_id):
    visit = Visit.query.get(visit_id) 

    if visit is None:
        status = 'Data not found'
        status_code = 404
    else:  # иначе удаляем студента
        db.session.delete(visit)
        db.session.commit()
        status = "Visit is deleted"
        status_code = 200

    return make_response(
        jsonify(status=status),
        status_code
    )


# ---------------STUDENT-------------

# ---GET---


@app.route('/students', methods=['GET'])
def get_all_students():
    students_all = Student.query.all()

    return make_response(
        jsonify(
            status='OK',
            students=[student.to_dict() for student in students_all]  # делаем список словарей
        ),
        200
    )


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    else:
        return make_response(
            jsonify(
                status='OK',
                student=student.to_dict()
            ),
            200
        )


@app.route('/students/group/<group_number>', methods=['GET'])
def get_group(group_number):
    # достаем всех студентов из заданной группы
    students = Student.query.filter_by(group_number=group_number).first()

    if students is None:
        return make_response(
            jsonify(status='Group not found'),
            404
        )

    else:
        students = Student.query.filter_by(group_number=group_number)
        return make_response(
            jsonify(
                status='OK',
                students=[student.to_dict() for student in students]  # делаем список словарей
            ),
            200
        )


# ---POST---


@app.route('/students', methods=['POST'])
def create_student():
    student_data = request.get_json(silent=True)

    if student_data is None:
        return make_response(
            jsonify(status="Invalid json"),
            400
        )

    try:
        name = student_data['name']
        group_number = student_data['group_number']
    except KeyError:
        return make_response(
            jsonify(status="Requires name and group_number values"),
            400
        )

    if not isinstance(name, str):
        return make_response(
            jsonify(status="name must be str value"),
            400
        )

    if not isinstance(group_number, str):
        return make_response(
            jsonify(status="group_number must be str value"),
            400
        )

    student = Student(name=name, group_number=group_number)
    try:
        db.session.add(student)
        db.session.commit()
        status_code = 200
        status = "Created"
    except IntegrityError:
        return make_response(
            jsonify(status='Found same student'),
            400
        )

    return make_response(
        jsonify(
            status=status,
            student=student.to_dict()
        ),
        status_code
    )


# ---PUT---


@app.route('/students/<int:student_id>', methods=['PUT'])
def edit_student(student_id):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    student_data = request.get_json(silent=True)

    if student_data is None:
        return make_response(
            jsonify(status="Invalid json"),
            400
        )

    try:
        name = student_data['name']
        group_number = student_data['group_number']
    except KeyError:
        return make_response(
            jsonify(status="Requires name and group_number values"),
            400
        )

    if not isinstance(name, str):
        return make_response(
            jsonify(status="name must be str value"),
            400
        )
    if not isinstance(group_number, str):
        return make_response(
            jsonify(status="group_number must be str value"),
            400
        )

    try:
        student.name = name
        student.group_number = group_number
        db.session.commit()
        status_code = 200
        status = 'Edited'
    except IntegrityError:
        return make_response(jsonify(
            status='Found the same student',
            ), 400)

    return make_response(
        jsonify(
            status=status,
            student=student.to_dict()
        ),
        status_code
    )


# ---DELETE---


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:
        status = 'Student not found'
        status_code = 404
    else:
        db.session.delete(student)
        db.session.commit()
        status = "Student is deleted"
        status_code = 200

    return make_response(
        jsonify(status=status),
        status_code
    )


if __name__ == '__main__':
    app.run()
