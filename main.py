from datetime import date, datetime
from models import db, Student, Visit
from flask import Flask, jsonify, make_response, request

from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db.init_app(app)

@app.route('/visits/<int:visit_id>', methods=['GET'])
def get_visit_by_id(visit_id):
    visit = Visit.query.get(visit_id)

    if visit is None:
        return make_response(jsonify(status="Visit not found"), 404)
    # на выходе {"status": "Visit not found"}

    return make_response(jsonify(
        status='OK',
        visit=visit.to_dict()
    ), 200)
    # на выходе {"status": "ok", "visit": {"id": 1, "date": "2017.01.01",
    # "pair_num": 1, "student_id": 10}}


@app.route('/visits', methods=['GET'])
def get_all_visits():
    visits = Visit.query.all()  # достаем все

    return make_response(jsonify(
        status='OK',
        visits=[visit.to_dict() for visit in visits]  # делаем список словарей
    ), 200)
    # на выходе что-то вроде
    # {"status": "OK", "visits": [{"id: 1, "pair_num": 1, ...}, ...]}


@app.route('/visits', methods=['POST'])
def create_visit():
    # request - глобальный контекст-зависимый объект запроса клиента
    # в момент прихода запроса - туда записываются все данные запроса (ip,
    # url, данные, тип запроса, ...)
    # с ним можно работать во вьюхе никак явно не передавая

    # http://flask.pocoo.org/docs/0.12/api/#flask.Request.get_json
    # проверяет что в заголовках запроса установлен жсон, если нет - None
    # пытается спарсить жсон в словарь, если не вышло - падает с исключением
    # silent=True заменяет исключение на возврат None
    visit_data = request.get_json(silent=True)

    if visit_data is None:
        return make_response(
            jsonify(status="Invalid json"),
            400
        )

    # для создания посещения нам нужен: студент, дата, номер пары, пробуем
    # извлечь, а также валидируем всё

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
        db.session.rollback()
        visit = Visit.query.filter_by(date=pair_date, pair_num=pair_num,
                                      student=student).first()
        status_code = 200
        status = "Found"

    return make_response(
        jsonify(status=status, visit=visit.to_dict()),
        status_code
    )


@app.route('/visits/student/<int:student_id>/date/<pair_date>/get', methods=['GET'])
def get_visits(student_id, pair_date):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:  # если студент не найден - вернуть ошибку.
        # Model.query.get возвращает None, если в базе нет записи с таким
        # примари-кей.
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        return 'Student not found', 404

    try:  # если дату не получилось спарсить, то strptime выкинет исключение
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
        # не забываем перевести datetime в date c помощью .date()
    except ValueError:  # ловим исключение, и прописываем действие
        return 'Invalid date format, try YYYY.MM.DD', 400

    visits_by_day = Visit.query.filter_by(student=student, date=pair_date).all()

    # заполняем все номера пар - False
    pair_visits = {1: False, 2: False, 3: False, 4: False}

    for visit in visits_by_day:  # перебираем все визиты студента за день
        pair_visits[visit.pair_num] = True  # если он был на этой паре,
        # то ставим True

    # если visits_by_day - пустая последовательность (ни одного визита не
    # было), то цикл не выполнится ни разу и все будут False (что логично)

    # возвращаем json-результат как договарились в #3
    return make_response(jsonify(visits={
        'student': student_id,
        'date': pair_date.strftime('%Y.%m.%d'),
        'pairs': pair_visits
    }), 200)


# должен работать и есть комментарии
@app.route('/visits/student/<int:student_id>/date/<pair_date>/pair/<int:pair_num>/post', methods=['POST'])
def post_visits(student_id, pair_date, pair_num):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:  # если студент не найден - вернуть ошибку.
        # Model.query.get возвращает None, если в базе нет записи с таким
        # примари-кей.
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        return 'Student not found', 404

    try:  # если дату не получилось спарсить, то strptime выкинет исключение
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
        # не забываем перевести datetime в date c помощью .date()
    except ValueError:  # ловим исключение, и прописываем действие
        return 'Invalid date format, try YYYY.MM.DD', 400

    # проверяем наличие данных о заданной паре
    visit = Visit.query.filter_by(student=student, date=pair_date,
                                  pair_num=pair_num).first()

    if visit is None:  # если посещение не найдено, то вносим его в базу
        visit = Visit(date=pair_date, pair_num=pair_num, student=student)
        db.session.add(visit)
        db.session.commit()
        return make_response(jsonify(stud={
            'student': student_id,
            'date': pair_date.strftime('%Y.%m.%d'),
            'pair': pair_num
        }), 201)
    else:  # иначе сообщаем о том, что данные уже существуют
        return 'Data is in the DataBase', 200


# работает и есть комментарии
@app.route('/visits/student/<int:student_id>/date/<pair_date>/pair/<int:pair_num>/delete', methods=['DELETE'])
def delete_visits(student_id, pair_date, pair_num):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:  # если студент не найден - вернуть ошибку.
        # Model.query.get возвращает None, если в базе нет записи с таким
        # примари-кей.
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        return 'Student not found', 404

    try:  # если дату не получилось спарсить, то strptime выкинет исключение
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
        pair_date = datetime.strptime(pair_date, '%Y.%m.%d').date()
        # не забываем перевести datetime в date c помощью .date()
    except ValueError:  # ловим исключение, и прописываем действие
        return 'Invalid date format, try YYYY.MM.DD', 400

    # проверяем наличие данных о заданной паре
    visit = Visit.query.filter_by(student=student, date=pair_date,
                                  pair_num=pair_num).first()

    if visit is None:  # если данные не найдены, сообщаем об этом
        return 'Data not found', 200
    else:  # иаче удаляем
        db.session.delete(visit)
        db.session.commit()
        return "Visit is deleted", 200  # сообщаем об удалении


# работает и есть комментарии
@app.route('/students/get', methods=['GET'])
def get_students():
    # достаем всех студетов
    students_all = Student.query.all()
    # создаем пустой словарь
    students = {}
    for student in students_all:
        students[student.id] = student.name  # запоняем имеющимися у нас данными
    # возвращаем json-результат
    return make_response(jsonify(student={'group': 'All', 'name': students}), 200)


# работает и есть комментарии
@app.route('/students/<int:student_id>/get', methods=['GET'])
def get_student_by_id(student_id):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:  # если студент не найден - вернуть ошибку.
        # Model.query.get возвращает None, если в базе нет записи с таким
        # примари-кей.
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        return 'Student not found', 404
    else:  # иначе возвращаем информацию о студенте
        return make_response(jsonify(student={
            'id': student.id,
            'group_number': student.group_number,
            'name': student.name
        }), 200)


# не работает и есть комментарии
@app.route('/students/<int:student_id>/put', methods=['PUT'])
def put_student(student_id, student_name, student_group):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)
    if student is None:  # если студент не найден, то ошибка
        return 'Student not found', 404
    else:  # иначе вносим изменения в базу
        db.session.delete(student)  # удаляем старые данные
        # записываем новые данные, ругается на id=student_id, удаляю тоже не работает
        student = Student(name=student_name, group_number=student_group)
        db.session.add(student)
        db.session.commit()
        # возвращаем json
        return make_response(jsonify(student={
            'id': student.id,
            'group_number': student.group_number,
            'name': student.name
        }), 200)


# работает и есть комментарии
@app.route('/delete/student/<int:student_id>/delete', methods=['DELETE'])
def delete_student(student_id):
    # вытаскиваем студента по id
    student = Student.query.get(student_id)

    if student is None:  # если студент не найден - вернуть ошибку.
        # Model.query.get возвращает None, если в базе нет записи с таким
        # примари-кей.
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get
        return 'Student not found', 404
    else:  # иначе удаляем студента
        db.session.delete(student)
        db.session.commit()
        return "Student is deleted", 200


# работает и есть комментарии
@app.route('/students/group/<group_number>/get', methods=['GET'])
def get_group(group_number):
    # достаем всех студентов из заданной группы
    students = Student.query.filter_by(group_number=group_number).all()
    if students is None:  # если нет ни одного студента в данной группе
        return 'Group not found', 404  # то возвращаем ошибку о том, что группа не найдена
    else:  # иначе создаем пустой словарь и заполняем имеющмися данными
        students = {}
        for student in students:
            students[student.id] = student.name
        # возвращаем json-результат
        return make_response(jsonify(student={'group': group_number, 'name': students_list}), 200)


if __name__ == '__main__':
    app.run()
