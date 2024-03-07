from users.views import UsersListView, UsersDetailView, UsersUpdateView, UsersDeleteView, UsersRegistrationView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

app_name = "users"

urlpatterns = [
    path("list/", UsersListView.as_view()),
    path("list/<int:pk>/", UsersDetailView.as_view()),
    path("update/<int:pk>/", UsersUpdateView.as_view()),
    path("delete/<int:pk>/", UsersDeleteView.as_view()),
    path("registration/", UsersRegistrationView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="take_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),

]