from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import requests

from config.settings import TELEGRAM_TOKEN
from habits.models import Habit
from users.models import User

DAYS_OF_WEEK = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def send_telegram_messages(messages):
    """
    Отправляет пакетное сообщение пользователю через Telegram.

    :param messages: Словарь с chat_id в качестве ключей и сообщениями в качестве значений.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    for chat_id, message in messages.items():
        params = {"chat_id": chat_id, "text": message}
        requests.get(url, params=params)


def check_habit(habit, current_time, today):
    """
    Проверяет выполнение привычки и добавляет сообщение в пакет при необходимости.

    :param habit: Экземпляр модели Habit, представляющий привычку.
    :param current_time: Текущее время.
    :param today: Строка с названием текущего дня недели.
    :return: Кортеж (chat_id, message) в случае выполнения привычки, иначе (None, None).
    """
    if habit.frequency == "DAILY" or habit.frequency == today:
        if habit.time.strftime("%H:%M") == current_time.strftime("%H:%M"):
            # Вывод информации о выполненной привычке
            print(f'ИНФОРМАЦИЯ О ПРИВЫЧКЕ: {habit}')

            chat_id = habit.owner.chat_id
            message = f"ДЕЙСТВИЕ: {habit.action}\nМЕСТО: {habit.place}\n"

            if habit.award:
                message += f"ВАША НАГРАДА: {habit.award}\n"
            elif habit.link_pleasant:
                message += f"СОЗДАЙТЕ ПРИЯТНУЮ ПРИВЫЧКУ: {habit.link_pleasant.action}\n"
            else:
                message += "НЕ ВЫБРАННА НАГРАДА ИЛИ ПРИЯТНАЯ ПРИВЫЧКА\n"

            message += f"ПРОДОЛЖИТЕЛЬНОСТЬ: {habit.duration}"
            return chat_id, message
    return None, None


def group_habits_by_time_and_day(habits):
    """
    Группирует привычки по времени и дню.

    :param habits: Список экземпляров модели Habit.
    :return: Словарь с ключами (time, frequency) и значениями списков привычек.
    """
    habits_by_time_and_day = defaultdict(list)
    for habit in habits:
        habits_by_time_and_day[(habit.time, habit.frequency)].append(habit)
    return habits_by_time_and_day


def build_combined_message(grouped_habits, current_time, today):
    """
    Создает объединенное сообщение на основе групп привычек.

    :param grouped_habits: Список привычек, сгруппированных по времени и дню.
    :param current_time: Текущее время.
    :param today: Строка с названием текущего дня недели.
    :return: Кортеж (список chat_ids, объединенное сообщение).
    """
    combined_message = ""
    chat_ids = []
    for habit in grouped_habits:
        chat_id, message = check_habit(habit, current_time, today)
        if chat_id and message:
            chat_ids.append(chat_id)
            combined_message += message + "\n\n"
    return chat_ids, combined_message


def habit_scheduler() -> None:
    """
    Проверяет время/день выполнения привычек и отправляет уведомления пользователям.
    """
    current_time = datetime.now()
    today = DAYS_OF_WEEK[datetime.today().weekday()]

    habits = Habit.objects.filter(is_pleasant=False, frequency__in=["DAILY", today])
    habits_by_time_and_day = group_habits_by_time_and_day(habits)

    messages = {}
    for (time, frequency), grouped_habits in habits_by_time_and_day.items():
        chat_ids, combined_message = build_combined_message(grouped_habits, current_time, today)
        if chat_ids and combined_message:
            for chat_id in chat_ids:
                messages[chat_id] = combined_message
    send_telegram_messages(messages)


def telegram_check_updates() -> None:
    """
    Получает информацию от Telegram бота и добавляет идентификатор пользователя в базу данных.
    """
    url_get_updates = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    response = requests.get(url_get_updates)

    if response.status_code == 200:
        for telegram_users in response.json()["result"]:
            telegram_user_chat_id = telegram_users["message"]["from"]["id"]
            telegram_user_name = telegram_users["message"]["from"]["username"]

            try:
                user = User.objects.get(telegram_user_name=telegram_user_name)
                if user.chat_id is None:
                    user.chat_id = telegram_user_chat_id
                    user.save()
            except ObjectDoesNotExist:
                print("Пользователь не найден в базе данных.")
