from datetime import date
from models import db, Student, Visit
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db.init_app(app)
app.app_context().push()
db.create_all()

student = Student(name='Rick', group_number='161')
db.session.add(student)
student = Student(name='Morty', group_number='162')
db.session.add(student)
db.session.commit()

Rick = Student.query.filter_by(name='Rick').first()
visit = Visit(date=date(2017, 9, 1), pair_num='2', student=Rick)
db.session.add(visit)
visit = Visit(date=date(2017, 9, 5), pair_num='4', student=Rick)
db.session.add(visit)

Morty = Student.query.filter_by(name='Morty').first()
visit = Visit(date=date(2017, 9, 1), pair_num='2', student=Morty)
db.session.add(visit)
visit = Visit(date=date(2017, 9, 1), pair_num='3', student=Morty)
db.session.add(visit)
db.session.commit()

Rick = Student.query.filter_by(name='Rick').first()
print(list(Visit.query.filter_by(student=Rick).all()))  # Пары, на которых был Рик
print(list(Visit.query.filter_by(date=date(2017, 9, 1)).all()))  # Все посещения за 1 сентября

