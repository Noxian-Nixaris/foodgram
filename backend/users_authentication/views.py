from djoser.views import UserViewSet

from .serializers import CreateUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CreateUserSerializer
