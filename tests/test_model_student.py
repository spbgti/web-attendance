from models import Student


def test_student_to_dict(db):
    """
        Проверяет что to_dict у Student работает ожидаемо
    """
    student = Student(name='Ivan', group_number='111')
    student.save()
    expected = {'id': 1, 'name': 'Ivan', 'group_number': '111'}
    # сравниваем
    assert student.to_dict() == expected
