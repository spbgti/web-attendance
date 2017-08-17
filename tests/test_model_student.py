from models import Student


def test_student_to_dict(db):
    student = Student(name='Ivan', group_number='111')
    db.session.add(student)
    db.session.commit()
    expected = {'id': 1, 'name': 'Ivan', 'group_number': '111'}
    # сравниваем
    assert student.to_dict() == expected
