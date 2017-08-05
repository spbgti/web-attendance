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

Rick = Visit(date='01.09.17', pair_num='2', student=student)
db.session.add(Rick)
Rick = Visit(date='05.09.17', pair_num='4', student=student)
db.session.add(Rick)

Morty = Visit(date='01.09.17', pair_num='2', student=student)
db.session.add(Morty)
Morty = Visit(date='01.09.17', pair_num='3', student=student)
db.session.add(Morty)
db.session.commit()

Rick = Student.query.filter_by(name='Rick').first()
print(list(Visit.query.filter_by(student=Rick).all()))  # Пары, на которых был Рик
print(list(Visit.query.filter_by(date='01.09.17').all()))  # Все посещения за 1 сентября
