from models import Visit, Student
from datetime import date


def test_visit_to_dict(db):
    """
    Проверяет что to_dict у Visit работает ожидаемо

    """
    student = Student(name='Маша', group_number='111')
    db.session.add(student)
    db.session.commit()
    visit = Visit(student=student, date=date(2006, 6, 6), pair_num=1)
    db.session.add(visit)
    db.session.commit()
    # что должны получить
    expected = {'id': 1, 'student_id': 1, 'date': '2006.06.06', 'pair_num': 1}
    # сравниваем
    assert visit.to_dict() == expected
