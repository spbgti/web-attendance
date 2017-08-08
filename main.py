from datetime import date, datetime
from models import db, Student, Visit
from flask import Flask, jsonify, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db.init_app(app)


@app.route('/visits/student/<int:student_id>/date/<pair_date>', methods=['GET'])
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
    return jsonify(visits={
        'student': student_id,
        'date': pair_date.strftime('%Y.%m.%d'),
        'pairs': pair_visits
    })


# исправить эндпоинт
@app.route('/visits/student/<int:student_id>/date/<pair_date>/pair/<int:pair_num>/add', methods=['POST'])
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
    visit = Visit.query.filter_by(student=student, date=pair_date, pair_num=pair_num).all()

    if visit is None:
        visit = Visit(date=pair_date, pair_num=pair_num, student=student)
        db.session.add(visit)
        db.session.commit()
        return 'Add:', jsonify(student), 200  # надо ли добавлять более подробные сведения
    else:
        return 'Data is in the DataBase', 200


@app.route('/visits/student/<int:student_id>/date/<pair_date>/pair/<int:pair_num>', methods=['DELETE'])
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
    visit = Visit.query.filter_by(student=student, date=pair_date, pair_num=pair_num).all()

    if visit is None:
        return 'Data not found', 200
    else:
        visit = Visit.query.filter_by(student=student, date=pair_date, pair_num=pair_num).delete()
        return 'Data deleted', jsonify(student), 200


@app.route('/students', methods=['GET'])
def get_students(*args):
    if args is None:
        students_all = Student.query.all()
    else:
        students_all = Student.query.flter_by(group_number=args).all()
    # возвращаем json-результат
    return jsonify(students_all), 200


@app.route('/students/group/<group_number>', methods=['GET_GROUP'])
def get_group(group_number):
    if get_students(group_number) is None:
        return 'Group not found', 404
    else:
        get_students(group_number)


if __name__ == '__main__':
    app.run()
