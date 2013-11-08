'''
API Endpoint ViewSets
'''
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.permissions import DjangoObjectPermissions

from api.models import CheckList
from api.serializers import CheckListSerializer


class CheckListViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the CheckList model
    '''
    allowed_methods = ['GET', 'POST', ]
    model = CheckList
    permission_classes = (DjangoObjectPermissions, )
    serializer_class = CheckListSerializer

    def post_save(self, obj, created=False):
        """
        Actions to perform immediately after saving a CheckList
        """
        if created:
            assign_perm('change_checklist', obj.owner, obj)
            assign_perm('delete_checklist', obj.owner, obj)
            assign_perm('view_checklist', obj.owner, obj)


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
