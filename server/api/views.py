"""
API Endpoint ViewSets
"""
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework import viewsets
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response

from api.models import CheckList
from api.serializers import CheckListSerializer


class CheckListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CheckList model
    """
    allowed_methods = ['GET', 'POST', ]
    model = CheckList
    permission_classes = (DjangoObjectPermissions, )
    serializer_class = CheckListSerializer

    def post_save(self, obj, created=False):
        """
        Actions to perform immediately after saving a CheckList
        """
        if created:
            assign_perm('api.change_checklist', obj.owner, obj)
            assign_perm('api.delete_checklist', obj.owner, obj)
            assign_perm('api.view_checklist', obj.owner, obj)

    def list(self, request):
        """
        Override the default list() method

        filter queryset by owner
        """
        check_lists = get_objects_for_user(
                request.user,
                ['api.view_checklist', ],
                )
        serializer = CheckListSerializer(check_lists, many=True, )
        return Response(serializer.data)


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
