from datetime import datetime, timedelta

from flask import jsonify, make_response, request, Blueprint
from sqlalchemy.exc import IntegrityError

from models import db, Student, Visit

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.route('/visits/<int:visit_id>', methods=['GET'])
def get_visit_by_id(visit_id: int):
    """
    Ищет соответствующий идентификатору оъект Visit
    :param visit_id: идентификатор объекта
    :return: если объект найден, возвращает его json-представление, если не найден - возвращает ошибку
    """
    visit = Visit.query.get(visit_id)

    if visit is None:
        return make_response(
            jsonify(status="Visit not found"),
            404
        )

    return make_response(
        jsonify(
            status='OK',
            visit=visit.to_dict()
        ),
        200
    )


@api.route('/visits', methods=['GET'])
def get_all_visits():
    """
    Возвращает все объекты Visit, сохраненные в базе данных
    :return: возвращает массив json-представлений каждого объекта
    """
    visits = Visit.query.all()

    return make_response(
        jsonify(
            status='OK',
            visits=[visit.to_dict() for visit in visits]
        ),
        200
    )


@api.route('/visits/student/<int:student_id>/date/<pair_date>', methods=['GET'])
def get_visits_by_day(student_id: int, pair_date: str):
    """
    Ищет студента по student_id и возвращает данный о посещении 4 пар за указанный день
    :param student_id: идентификатор, связывающий объекты Student и Visit
    :param pair_date: строка формата YYYY.MM.DD
    :return: если объект найден, возвращает его json-представление с данными о посещении 4 пар, если не найден - возвращает ошибку
    """
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:
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


@api.route('/visits/student/<int:student_id>/week/<week_start>', methods=['GET'])
def get_visits_by_week(student_id: int, week_start: str):
    """
    Получение информации о посещениях студента за неделю(7 дней)
    :param student_id: идентификатор, связывающий объекты Student и Visit
    :param week_start: строка формата YYYY.MM.DD
    :return: если объект найден, возвращает json-представление с данными о посещении в 7 дней, начиная с переданного включительно,
             если не найден - возвращает ошибку
    """
    student = Student.query.get(student_id)

    if student is None:
        return make_response(
            jsonify(status='Student not found'),
            404
        )

    try:
        week_start = datetime.strptime(week_start, '%Y.%m.%d').date()
    except ValueError:
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

        visits_by_week[week_start.strftime('%Y.%m.%d')] = pair_visits
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


@api.route('/visits', methods=['POST'])
def create_visit():
    """
    Валидирует данный, передаваемые json-ом через POST, создает и сохраняет новый Visit
    :return: если успешно, возвращает json-представление созданного Visit,  иначе - ошибку
    """
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

    if not isinstance(student_id, int):
        return make_response(
            jsonify(status="student_id must be int value"),
            400
        )

    student = Student.query.get(student_id)
    if student is None:
        return make_response(
            jsonify(status="Student not found"),
            404
        )

    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:
        return make_response(
            jsonify(status="Invalid date format, try YYYY.MM.DD"),
            400
        )

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

    visit = Visit.query.filter_by(date=pair_date, pair_num=pair_num, student=student).first()

    if visit is None:
        visit = Visit(date=pair_date, pair_num=pair_num, student=student)
        visit.save()
        status_code = 201
        status = "Created"
    else:
        status_code = 400
        status = 'Found the same visit'

    return make_response(
        jsonify(
            status=status,
            visit=visit.to_dict()
        ),
        status_code
    )


@api.route('/visits/<int:visit_id>', methods=['PUT'])
def edit_visit(visit_id: int):
    """
    Валидирует данный, передаваемые json-ом через PUST, обновляет объект Visit, найденный по visit_id базе
    :param visit_id: идентифкатор объекта Visit
    :return: если успешно, возвращает json-представление измененного Visit,  иначе - ошибку
    """
    visit = Visit.query.get(visit_id)

    if visit is None:
        return make_response(
            jsonify(status="Visit not found"),
            404
        )

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

    if not isinstance(student_id, int):
        return make_response(
            jsonify(status="student_id must be int value"),
            400
        )

    student = Student.query.get(student_id)
    if student is None:
        return make_response(
            jsonify(status="Student not found"),
            404
        )

    try:
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
    except ValueError:
        return make_response(
            jsonify(status="Invalid date format, try YYYY.MM.DD"),
            400
        )

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

    new_visit = Visit.query.filter_by(date=pair_date, pair_num=pair_num, student=student).first()

    if new_visit is None:
        visit.student_id = student_id
        visit.date = pair_date
        visit.pair_num = pair_num
        visit.save()
        status_code = 200
        status = "Edited"
    else:
        visit = new_visit
        status_code = 400
        status = 'Found the same visit'

    return make_response(
        jsonify(
            status=status,
            visit=visit.to_dict()
        ),
        status_code
    )


@api.route('/visits/<int:visit_id>', methods=['DELETE'])
def delete_visit(visit_id: int):
    """
    Находит объект Visit по visit_id и удаляет его из базы данных
    :param visit_id: идентификатор объекта Visit
    :return: если объект найден, сообщает о его удалении, иначе возвращает ошибку
    """
    visit = Visit.query.get(visit_id)

    if visit is None:
        status = 'Visit not found'
        status_code = 404
    else:
        visit.delete()
        status = "Visit is deleted"
        status_code = 200

    return make_response(
        jsonify(status=status),
        status_code
    )


@api.route('/students', methods=['GET'])
def get_all_students():
    """
    Возвращает все объекты Student, сохраненные в базе данных
    :return: массив из json-представлений Student
    """
    students_all = Student.query.all()

    return make_response(
        jsonify(
            status='OK',
            students=[student.to_dict() for student in students_all]
        ),
        200
    )


@api.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id: int):
    """
    Ищет соответсвующий идентификатору объект Student
    :param student_id: идентификатор объекта Student
    :return: если объект найден, возвращает его json-представление, если не найден - возвращает ошибку
    """
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


@api.route('/students/group/<group_number>', methods=['GET'])
def get_students_by_group(group_number: int):
    """
    Ищет объекты Student по group_number и возвращает даные о них
    :param group_number: группа, в которой состоят студенты
    :return: если группа найдена возвращает массив из json-представлений о студентах, иначе - ошибку
    """
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
                students=[student.to_dict() for student in students]
            ),
            200
        )


@api.route('/students', methods=['POST'])
def create_student():
    """
    Валидирует данные, передаваемые json-ом через POST, создает и сохраняет новый Student
    :return: если успешно - json-представление созданного Student, иначе - ошибку
    """
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

    student = Student.query.filter_by(name=name, group_number=group_number).first()

    if student is None:
        student = Student(name=name, group_number=group_number)
        student.save()
        status_code = 201
        status = "Created"
    else:
        status_code = 400
        status = 'Found same student'

    return make_response(
        jsonify(
            status=status,
            student=student.to_dict()
        ),
        status_code
    )


@api.route('/students/<int:student_id>', methods=['PUT'])
def edit_student(student_id: int):
    """
    Валидирует данные, передаваемые json-ом через POST и обновляет объект Student, найденный по student_id в базе
    :param student_id: идентификатор объекта Student
    return: если успешно - json-представление обновленного Student, иначе - ошибку
    """
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

    new_student = Student.query.filter_by(name=name, group_number=group_number).first()

    if new_student is None:
        student.name = name
        student.group_number = group_number
        student.save()
        status_code = 200
        status = 'Edited'

    else:
        student = new_student
        status_code = 400
        status = 'Found same student'

    return make_response(
        jsonify(
            status=status,
            student=student.to_dict()
        ),
        status_code
    )


@api.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id: int):
    """
    Находит объект Student по student_id и удаляет его из базы данных
    :param student_id: идентификатор объекта Student
    :return: если объект найден, сообщает о его удалении, иначе возвращает ошибку
    """
    student = Student.query.get(student_id)

    if student is None:
        status = 'Student not found'
        status_code = 404
    else:
        student.delete()
        status = "Student is deleted"
        status_code = 200

    return make_response(
        jsonify(status=status),
        status_code
    )
