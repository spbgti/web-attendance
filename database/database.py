from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper

metadata = MetaData()
student_table = Table('student', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String),
                      Column('group_number', String)
                      )

class student(object):
    def __init__(self, id, name, group_number):
        self.id = id
        self.name = name
        self.group_number = group_number

mapper(student, student_table)

visit_table = Table('visit', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('date', Integer),
                    Column('pair_num', String),
                    Column('student', Integer, foreign_key=True)
                    )

class visit(object):
    def __init__(self, id, date, pair_num, student_key):
        self.id = id
        self.date = date
        self.pair_num = pair_num
        self.student_key = student_key

mapper(visit, visit_table)
