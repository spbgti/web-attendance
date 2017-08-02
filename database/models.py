from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True),
    name = db.Column(db.String)
    group_number = db.Column(db.String)

    def __repr__(self):
        return '<Student: %s, %s>' % (self.name, self.group_number)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True),
    date = db.Column(db.String)
    pair_num = db.Column(db.Integer)
    student_key = db.Column(db.Integer, foreign_key = True)

    def __repr__(self):
        return '<Visit: %s, %s, %s>' % (self.student_key, self.date, self.pair_num)
