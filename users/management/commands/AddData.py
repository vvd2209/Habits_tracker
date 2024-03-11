from django.core.management import BaseCommand

from users.management.commands.AddHabit import Command as AddHabit
from users.management.commands.AddGroupAndUser import Command as AddGroupAndUser


class Command(BaseCommand):
    help = 'Запускает все команды из users'

    def handle(self, *args, **options):
        # Вызываем команду AddGroupAndUser
        add_group_and_user_command = AddGroupAndUser()
        add_group_and_user_command.handle(*args, **options)

        # Вызываем команду AddGroupAndUser
        add_group_and_user_command = AddHabit()
        add_group_and_user_command.handle(*args, **options)
        