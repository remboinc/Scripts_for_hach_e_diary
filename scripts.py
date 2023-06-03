import random
from commendations import COMMENDATIONS
from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Commendation, Subject, Teacher


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid)
    return marks.filter(points__in=['2', '3']).update(points='5')


def remove_chastisements(schoolkid):
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    return chastisement.delete()


def create_commendation(schoolkid, lesson):
    comment = random.choice(COMMENDATIONS)
    subject = Subject.objects.get(title=lesson, year_of_study=6)
    lesson_object = Lesson.objects.filter(
        subject=subject,
        group_letter='А').order_by('?').first()
    date = lesson_object.date
    teacher_info = lesson_object.teacher
    teacher_full_name = teacher_info.full_name
    teacher = Teacher.objects.get(full_name=teacher_full_name)
    return Commendation.objects.create(
        text=comment,
        created=date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )


def main():
    schoolkid_full_name = input("Введите ФИО ученика: ")
    lesson = input("Введите название предмета: ")

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, lesson)
        print("Все прошло успешно")
    except Schoolkid.DoesNotExist:
        print("Такого ученика не удалось найти")
    except Schoolkid.MultipleObjectsReturned:
        print("Нашлось несколько учеников. Уточните, какого имеете ввиду")
    except AttributeError:
        print("Не нашлось такого предмета. Введите верное название, например, Музыка")


if __name__ == '__main__':
    main()
