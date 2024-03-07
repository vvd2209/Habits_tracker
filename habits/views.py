from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.pagination import DataPaginator
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner


class HabitListView(generics.ListAPIView):
    """
    Сериализатор для получения списка привычек.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = DataPaginator

    def get_queryset(self):
        user = self.request.user
        search_owners = []
        owners = Habit.objects.filter()
        # Поиск и фильтрация привычек пользователей
        for find_owner in owners:
            if find_owner.is_public is True:
                search_owners.append(find_owner)
            else:
                if find_owner.owner == user:
                    search_owners.append(find_owner)
        return search_owners


class HabitDetailView(generics.RetrieveAPIView):
    """
    Сериализатор для получения деталей привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitCreateView(generics.CreateAPIView):
    """
    Сериализатор для создания новой привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateView(generics.UpdateAPIView):
    """
    Сериализатор для обновления информации о привычке.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDeleteView(generics.DestroyAPIView):
    """
    Сериализатор для удаления привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ShareHabitListView(generics.ListAPIView):
    """
    Сериализатор для получения списка общедоступных привычек.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        owners = Habit.objects.filter(is_public=True)
        return owners
