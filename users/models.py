from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель представления класса Пользователь, наследуемая от абстрактного класса
    """
    username = None  # исключение поля "username", так как вместо него будет использовано поле "email"

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты пользователя")
    chat_id = models.IntegerField(unique=True, blank=True, null=True, default=None, verbose_name="Идентификатор чата")
    telegram_user_name = models.CharField(max_length=100, null=False, blank=False, unique=True,
                                          verbose_name="Имя пользователя в Telegram")

    USERNAME_FIELD = "email"  # указание на то, что поле "email" будет использоваться для идентификации пользователя
    REQUIRED_FIELDS = []  # поля, которые будут запрашиваться при создании пользователя через команду createsuperuser

    def __str__(self):
        """
        Метод представления модели в виде строки
        """
        return f"{self.email}"

    class Meta:
        """
        Метаданные модели
        """
        verbose_name = "пользователь"
        verbose_name_plural = 'пользователи'
