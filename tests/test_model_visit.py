from datetime import date

from models import Visit, Student


def test_visit_to_dict(db):
    """
    Проверяет что to_dict у Visit работает ожидаемо

    """
    student = Student(name='Маша', group_number='111')
    student.save()
    visit = Visit(student=student, date=date(2006, 6, 6), pair_num=1)
    visit.save()
    # что должны получить
    expected = {'id': 1, 'student_id': 1, 'date': '2006.06.06', 'pair_num': 1}
    # сравниваем
    assert visit.to_dict() == expected
