from django.core.management import BaseCommand
from habits.models import Habit

test_nice_habits = [
    {
        "id": 1,
        "user_id": 1,
        "place": "home",
        "action": "eat desert"
    }
]

test_habits = [
    {
        "id": 1,
        "user_id": 1,
        "place": "home",
        "time": "12:00",
        "action": "drink water",
        "reward": "10 DKK",
        "periodicity": 1,
        "is_public": False,
        "duration_time": "00:00:15",
    },
    {
        "id": 2,
        "user_id": 1,
        "place": "home",
        "time": "12:00",
        "action": "not drink alcohol",
        "reward": "15 DKK",
        "periodicity": 1,
        "is_public": False,
        "duration_time": "00:00:15",
    },
    {
        "id": 3,
        "user_id": 1,
        "place": "home",
        "time": "12:00",
        "action": "clean restroom",
        "associated_nice_habit_id": 1,
        "periodicity": 3,
        "is_public": False,
        "duration_time": "00:00:15",
    },
]


class Command(BaseCommand):
    """Adding test habits in Database"""
    def handle(self, *args, **options):
        Habit.objects.all().delete()
        Habit.objects.all().delete()
        print('Old habits were deleted')
        for test_nice_habit in test_nice_habits:
            new_nice_habit = Habit.objects.create(**test_nice_habit)
            new_nice_habit.save()
        for test_habit in test_habits:
            new_habit = Habit.objects.create(**test_habit)
            new_habit.save()
        print('Test habits were added in database')
