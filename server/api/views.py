'''
API Endpoint ViewSets
'''
from django.contrib.auth.models import Group, User
from guardian.shortcuts import assign_perm
from rest_framework import viewsets

from api.models import CheckList
from api.serializers import CheckListSerializer


class CheckListViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the CheckList model
    '''
    model = CheckList
    serializer_class = CheckListSerializer

    def post_save(self, obj, created=False):
        if created:
            assign_perm('change_obj_checklist', obj.owner, obj)
            assign_perm('delete_obj_checklist', obj.owner, obj)
            assign_perm('view_obj_checklist', obj.owner, obj)


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
