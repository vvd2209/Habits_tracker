from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from users.models import User
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserSerializer, UserRegisterSerializer


class IsOwnerOrReadOnly(BasePermission):
    """
    Сериализатор для проверки, является ли пользователь
    владельцем объекта или ему разрешены только безопасные методы.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.pk == request.user.pk


class UsersListView(generics.ListAPIView):
    """
    Сериализатор для получения списка пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersDetailView(generics.RetrieveAPIView):
    """
    Сериализатор для получения деталей пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersCreateView(generics.CreateAPIView):
    """
    Сериализатор для создания нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersUpdateView(generics.UpdateAPIView):
    """
    Сериализатор для обновления информации пользователя.
    Разрешено только владельцу объекта.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UsersDeleteView(generics.DestroyAPIView):
    """
    Сериализатор для удаления пользователя.
    Разрешено только владельцу объекта.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UsersRegistrationView(generics.CreateAPIView):
    """
    Сериализатор для регистрации нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)
