from celery import shared_task
import requests
from django.conf import settings

from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from habits.models import Habit

bot_token = TELEGRAM_TOKEN
telegram_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'


@shared_task
def send_message_to_bot():
    """ Функция отправки сообщения в телеграм-бот
    chat_id: id чата
    message: передаваемое сообщение
    """
    habit = Habit.objects.get()
    requests.get(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
        params={
            'chat_id': habit.user.telegram_id,
            'text': f'Привет {habit.owner}! Время {habit.time}. Пора идти в {habit.place} и сделать {habit.action}. ' \
                    f'Это займет {habit.duration} минут!'
        }
    )
