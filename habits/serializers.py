from habits.models import Habit
from rest_framework import serializers


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для привычки с валидацией.
    """

    def create(self, validated_data):
        """
        Создание экземпляра привычки с валидацией данных.

        Args:
            validated_data (dict): Валидированные данные для создания привычки.

        Returns:
            Habit: Созданный экземпляр привычки.

        Raises:
            serializers.ValidationError: Если нарушены условия валидации.
        """
        new_habit = Habit.objects.create(**validated_data)

        # Проверка продолжительности
        if new_habit.duration > 120:
            raise serializers.ValidationError("Продолжительность больше 120 минут!")

        # Проверка обычной привычки
        if not new_habit.is_pleasant:
            if not new_habit.award:
                if not new_habit.link_pleasant:
                    raise serializers.ValidationError("Обычная привычка должна иметь награду или быть приятной! "
                                                      "Поле: award или link_pleasant")
            else:
                if new_habit.link_pleasant:
                    raise serializers.ValidationError(
                        "Обычная привычка не может одновременно иметь награду и быть приятной!")
        # Проверка приятной привычки
        else:
            if new_habit.award:
                raise serializers.ValidationError("Приятная привычка не может иметь награду!")

        return new_habit

    class Meta:
        model = Habit
        fields = "__all__"
