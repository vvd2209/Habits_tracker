import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from habits.models import Habit


class Command(BaseCommand):
    help = 'Заполняет базу данных 5 разными привычками'

    def handle(self, *args, **kwargs):
        for _ in range(5):
            action = f"Какое-то действие {_}"
            place = "Какое-то место"

            # Пытаемся получить привычку или создать новую, если не существует
            habit, created = Habit.objects.get_or_create(
                action=action,
                place=place,
                defaults={
                    'owner_id': None,  # Здесь вы можете указать конкретного пользователя
                    'time': timezone.now().time(),
                    'is_pleasant': random.choice([True, False]),
                    'link_pleasant': None,  # Здесь вы можете указать ссылку на другую приятную привычку
                    'frequency': random.choice([choice[0] for choice in Habit.HabitFrequency.choices]),
                    'award': f"Какая-то награда {_}",
                    'duration': 30,  # Продолжительность в минутах
                    'is_public': random.choice([True, False]),
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана новая привычка: {habit}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Привычка с действием "{action}" и местом "{place}" уже существует'))
