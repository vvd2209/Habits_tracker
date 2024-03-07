from django.db import models
from config import settings
from django.utils import timezone


class Habit(models.Model):
    """
    Модель представления класса Привычка
    """
    objects = None

    class HabitFrequency(models.TextChoices):
        """
        Класс вариантов частоты выполнения привычки
        """
        Daily = 'DAILY'
        monday = 'MONDAY'
        tuesday = 'TUESDAY'
        wednesday = 'WEDNESDAY'
        thursday = 'THURSDAY'
        friday = 'FRIDAY'
        saturday = 'SATURDAY'
        sunday = 'SUNDAY'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name="Владелец привычки")
    place = models.CharField(max_length=100, null=False, blank=False, verbose_name="Место привычки")
    time = models.TimeField(default=timezone.now, verbose_name="Время привычки")
    action = models.CharField(max_length=100, null=False, blank=False, verbose_name="Действие привычки")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    link_pleasant = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name='Связанная приятная привычка')
    frequency = models.CharField(choices=HabitFrequency.choices, default=HabitFrequency.Daily,
                                 verbose_name="Частота выполнения")
    award = models.CharField(max_length=100, null=True, blank=True, verbose_name="Награда за привычку")
    duration = models.IntegerField(null=False, blank=False, verbose_name="Продолжительность привычки")
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        """
        Метод представления модели в виде строки
        """
        return f"ДЕЙСТВИЕ: {self.action} МЕСТО: {self.place}"

    class Meta:
        """
        Метаданные модели
        """
        verbose_name = "привычка"
        verbose_name_plural = 'привычки'
