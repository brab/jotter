'''
API Endpoint ViewSets
'''
from django.contrib.auth.models import Group, User

from rest_framework import viewsets

from api.models import CheckList


class CheckListViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the CheckList model
    '''
    model = CheckList


class GroupViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the Group model
    '''
    model = Group


class UserViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the User model
    '''
    model = User
