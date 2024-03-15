from rest_framework.serializers import ValidationError


def validator_for_habit(value):
    """ Проверка на правильность заполнения полей привычки """

    try:
        if value['is_pleasant']:
            if value['link_pleasant'] or value['award']:
                raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
    except KeyError:
        pass

    try:
        if value['link_pleasant'] and value['award']:
            raise ValidationError('Можно выбрать или приятную привычку или вознаграждение')
    except KeyError:
        pass

    try:
        if value['duration'] > 2:
            raise ValidationError('Привычку можно выполнять не более 2 минут')
    except KeyError:
        pass

    try:
        if value['link_pleasant']:
            if not value['link_pleasant'].habit_is_good:
                raise ValidationError('В связанные привычки могут попадать только приятные привычки')
    except KeyError:
        pass
