from celery import shared_task
from habits.services import telegram_check_updates, habit_scheduler


# Задача Celery для проверки времени выполнения привычек и отправки уведомлений пользователям
@shared_task()
def check_habit_time():
    """
    Проверяет время выполнения привычек и отправляет уведомления пользователям через Telegram.
    """
    telegram_check_updates()  # Проверка обновлений от Telegram бота и обновление данных пользователей
    habit_scheduler()  # Планирование проверки времени выполнения привычек и отправка уведомлений
