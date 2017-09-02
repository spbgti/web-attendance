from flask import jsonify, make_response, Blueprint, request, redirect, url_for, render_template
from flask.ext.login import LoginManager

from flask_login import login_user, login_required, logout_user

from models import Student

auth = Blueprint('auth', __name__, url_prefix='/auth/v1')

lm = LoginManager()
lm.init_app(auth)


@lm.user_loader
def load_user(student_id):
    return Student.query.get(student_id)


@auth.route('/index', methods=['GET'])
def auth_student(student_id: int):
    """
    :param student_id: идентефикатор объекта
    :return: возвращает имя студента, если он авторизован и "auth required" если пользователь неавторизован
    """
    student = Student.query.get(student_id)
    if student is None:
        return make_response(
            jsonify(status="auth required"),
            400
        )
    else:
        return make_response(
            jsonify(
                status="OK",
                information=student.name
            ),
            200
        )


@auth.route('/login/<int:student_id>', methods=['GET', 'POST'])
def login_student(student_id: int):
    """
    Авторизация пользователя
    :param student_id:
    :return:
    """
    if request.method == "POST":
        student_id = request.form["login"]
        remember_me = request.form["remember"]
        # ищем пользователя по логину и паролю
        # get_user - внутренняя функция, для запроса к БД, например
        user = Student.query.get(student_id)
        if user:
            # если пользователь с тамим логином и паролем существует -
            # авторизуем и делаем редирект
            login_user(user, remember=remember_me)
            return redirect(url_for("index"))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Разлогинивает пользователя, удаляет куки из сессии
    :return:
    """
    logout_user()
    return redirect(url_for("index"))
