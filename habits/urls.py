from django.urls import path
from habits.views import (HabitListView, HabitDetailView, HabitCreateView, HabitUpdateView, HabitDeleteView,
                          ShareHabitListView)

app_name = "habits"

urlpatterns = [
    path("habits/", HabitListView.as_view(), name="list_all_habits"),
    path("habit/<int:pk>/", HabitDetailView.as_view(), name="habit_show"),
    path("habit/create/", HabitCreateView.as_view(), name="habit_create"),
    path("habit/update/<int:pk>/", HabitUpdateView.as_view(), name="habit_update"),
    path("habit/delete/<int:pk>/", HabitDeleteView.as_view(), name="habit_delete"),
    path("share_habits/", ShareHabitListView.as_view(), name="share_habits"),
]
