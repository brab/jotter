from django.contrib.auth.models import Group, User

from rest_framework import viewsets


class GroupViewSet(viewsets.ModelViewSet):
    model = Group


class UserViewSet(viewsets.ModelViewSet):
    model = User
