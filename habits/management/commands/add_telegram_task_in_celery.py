import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Adding task check_habits_for_action in Celery"""
    def handle(*args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name="Checking user's habits",
            task="habits.tasks.check_habits_for_action",
            kwargs=json.dumps({
                "be_careful": True,
            }),
            expires=datetime.utcnow() + timedelta(seconds=30)
        )
        