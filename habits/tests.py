from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from habits.models import Habit


class HabitTestCase(TestCase):

    def setUp(self):
        """ Подготовка к тестированию """
        self.user = User(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        self.user.set_password("test")
        self.user.save()

        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_habit(self):
        """ Тест создания привычки """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 30,
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.post("/drf/habit/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())

    def test_get_share_habits(self):
        """ Тест получения информации об общедоступных привычках """
        data = {
            "place": "На стадионе",
            "time": "16:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "award": "Выпить воды",
            "duration": 15,
            "is_public": True,
            "owner": 2
        }

        data2 = {
            "place": "На улице",
            "time": "08:00:00",
            "action": "Утренняя зарядка",
            "is_pleasant": True,
            "frequency": "WEDNESDAY",
            "award": "",
            "duration": 20,
            "is_public": True,
            "owner": 2
        }

        self.client.post("/drf/habit/create/", data)
        self.client.post("/drf/habit/create/", data2)
        response = self.client.get("/drf/share_habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_habits(self):
        """ Тест получения информации о привычках пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 30,
            "is_public": True,
            "owner": 1
        }

        data2 = {
            "place": "На стадионе",
            "time": "16:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "award": "Выпить воды",
            "duration": 15,
            "is_public": True,
            "owner": 1
        }

        self.client.post("/drf/habit/create/", data)
        self.client.post("/drf/habit/create/", data2)
        response = self.client.get("/drf/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_full_information_habit(self):
        """ Тест получения полной информации о привычке пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 30,
            "is_public": True,
            "owner": self.user.pk
        }

        self.client.post("/drf/habit/create/", data)
        habit_pk = Habit.objects.first().pk

        response = self.client.get(f"/drf/habit/{habit_pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        """ Тест обновления привычки пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 30,
            "is_public": True,
            "owner": self.user.pk
        }
        new_data = {
            "place": "В спортзале",
            "time": "17:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "award": "Выпить воды",
            "duration": 15,
            "is_public": True,
            "owner": self.user.pk
        }

        self.client.post("/drf/habit/create/", data)
        habit_pk = Habit.objects.first().pk
        response = self.client.put(f"/drf/habit/update/{habit_pk}/", new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_duration_create_habit(self):
        """ Тест на создание привычки с продолжительностью более 120 секунд """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 200,
            "is_public": True,
            "owner": 1
        }

        response = self.client.post("/drf/habit/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_pleasant_create_habit(self):
        """ Тест на создание приятной привычки с наградой """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": True,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 10,
            "is_public": True,
            "owner": 1
        }

        response = self.client.post("/drf/habit/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_usual_create_habit(self):
        """ Тест на создание обычной привычки без награды и приятности """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "duration": 10,
            "is_public": True,
            "owner": 1
        }

        response = self.client.post("/drf/habit/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_habit(self):
        """ Тест на удаления привычки """

        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "award": "Попить витаминный смузи",
            "duration": 30,
            "is_public": True,
            "owner": self.user.pk
        }

        self.client.post("/drf/habit/create/", data)
        habit_pk = Habit.objects.first().pk

        response = self.client.delete(f"/drf/habit/delete/{habit_pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validate_linked_create_habit(self):
        """ Тест на добавление связанной привычки с признаком is_pleasant = False """
        data_1 = Habit.objects.create(
            place="В парке",
            time="17:00:00",
            action="Пробежать 5 км",
            is_pleasant=False,
            frequency="SUNDAY",
            award="Попить витаминный смузи",
            duration=1,
            is_public=True,
            owner=self.user
        )

        data_2 = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "link_pleasant": data_1.pk,
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }
        response = self.client.post("/drf/habit/create/", data_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Habit.objects.all().exists())

    def test_validate_reward_and_linked_create_habit(self):
        """ Тест на создание привычки с наградой и связанной привычкой """
        data_1 = Habit.objects.create(
            place="В парке",
            time="17:00:00",
            action="Пробежать 5 км",
            is_pleasant=True,
            frequency="SUNDAY",
            award="Попить витаминный смузи",
            duration=1,
            is_public=True,
            owner=self.user
        )

        data_2 = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "link_pleasant": data_1.pk,
            "award": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        response = self.client.post("/drf/habit/create/", data_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Habit.objects.all().exists())
