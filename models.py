from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    group_number = db.Column(db.String)
    __table_args__ = (db.UniqueConstraint('name', 'group_number', name='Name_Group_UC'),)

    def __init__(self, name, group_number):
        self.name = name
        self.group_number = group_number

    def __repr__(self):
        return '<Student: %s, %s>' % (self.name, self.group_number)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_number': self.group_number
        }


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    pair_num = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student')
    __table_args__ = (db.UniqueConstraint('date', 'pair_num', 'student_id', name='Stud_Date_Pair_UC'),)

    def __init__(self, date, pair_num, student):
        self.date = date
        self.pair_num = pair_num
        self.student = student

    def __repr__(self):
        return '<Visit: %s, %s, %s>' % (self.student, self.date, self.pair_num)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y.%m.%d'),
            'pair_num': self.pair_num,
            'student_id': self.student_id
        }
