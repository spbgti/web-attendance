from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper

from database import metadata


db = SQLAlchemy()
# class Student(db.Model):
class Student(object):
    #    id = db.Column(db.Integer, primary_key=True),
    #    name = db.Column(db.String)
    #    group_number = db.Column(db.String)
    def __init__(self, name, group_number):
        self.name = name
        self.group_number = group_number

    def __repr__(self):
        return '<Student: %s, %s>' % (self.name, self.group_number)


students = Table('students', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('group_number', String)
                 )
mapper(Student, students)


# class Visit(db.Model):
class Visit(object):
    #    id = db.Column(db.Integer, primary_key=True),
    #    date = db.Column(db.String)
    #    pair_num = db.Column(db.Integer)
    #    student = db.Column(db.Integer)
    def __init__(self, date, pair_num, student):
        self.date = date
        self.pair_num = pair_num
        self.student = student

    def __repr__(self):
        return '<Visit: %s, %s, %s>' % (self.student, self.date, self.pair_num)


visits = Table('visits', metadata,
               Column('id', Integer, primary_key=True),
               Column('date', String),
               Column('pair_num', Integer),
               Column('student', Integer)
               )
mapper(Visit, visits)
