from models import db, Student, Visit
from flask import Flask
from database import init_db, db_session
from sqlalchemy import create_engine, MetaData, Table

app = Flask()

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'

db.init_app(app)

engine = create_engine('sqlite:///test.db', convert_unicode=True)
metadata = MetaData(bind=engine)

# Объявление таблиц
students = Table('students', metadata, autoload=True)
visits = Table('visits', metadata, autoload=True)

# Ручное добавление в БД
# s1 = Student('Ivan Ivanov', '161')
# db_session.add(s1)
# db_session.commit()
# s2 = Student('Petr Petrov', '261')
# db_session.add(s2)
# db_session.commit()
con = engine.connect()
con.execute(students.insert(), id=164000, name='Ivan Ivanov', group_number='161')
con.execute(students.insert(), id=164001, name='Petr Petrov', group_number='261')


# Закрытие сессии
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Ручное добавление в БД
# v1 = Visit('01.09.17', '1', 'Ivan Ivanov')
# db_session.add(v1)
# db_session.commit()
# v2 = Student('01.09.17', '2', 'Petr Petrov')
# db_session.add(v2)
# db_session.commit()
con = engine.connect()
con.execute(visits.insert(), date='01.09.17', pair_num=1, student=164000)
con.execute(visits.insert(), date='01.09.17', pair_num=2, student=164001)


# Закрытие сессии
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Запрос
result = students.select(students.c.id == 164000).execute().first()

db.init_app(app)
