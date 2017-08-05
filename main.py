from models import db, Student, Visit
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'

db.init_app(app)
app.app_context().push()


student = Student(name='Rick', group_number='161')
db.session.add(student)
db.commit()
Rick = Visit(date='01.09.17', pair_num='2', student=student)
db.session.add(Rick)
db.commit()
Rick = Visit(date='05.09.17', pair_num='4', student=student)
db.session.add(Rick)
db.commit()

student = Student(name='Morty', group_number='162')
db.session.add(student)
db.commit()
Morty = Visit(date='01.09.17', pair_num='2', student=student)
db.session.add(Morty)
db.commit()
Morty = Visit(date='01.09.17', pair_num='3', student=student)
db.session.add(Morty)
db.commit()

Rick = Student.query.filter(name='Rick').first()
print(list(Visit.query.filter(student=Rick).all))  # Пары, на которых был Рик
print(list(Visit.query.filter(date='01.09.17').all))  # Все посещения за 1 сентября
