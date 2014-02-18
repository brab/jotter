"""
API Endpoint ViewSets
"""
import os, subprocess

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from guardian.shortcuts import assign_perm, get_perms
from rest_framework import viewsets
from rest_framework.filters import DjangoObjectPermissionsFilter
from rest_framework.response import Response

from api.models import CheckList, CheckListItem
from api.permissions import JotterObjectPermissions
from api.serializers import CheckListSerializer, CheckListItemSerializer


class CheckListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CheckListItem model
    """
    model = CheckListItem
    serializer_class = CheckListItemSerializer

    def create(self, request, *args, **kw):
        if not request.user.is_authenticated():
            return Response(
                    data={
                        'detail': 'Authentication required',
                        },
                    status=403,
                    )

        check_list = CheckList.objects.get(id=request.DATA.get('check_list'))
        perms = get_perms(
                user_or_group=request.user,
                obj=check_list,
                )
        if 'change_checklist' not in perms:
            return Response(
                    data={
                        'detail': 'Permission denied',
                        },
                    status=403,
                    )

        return super(CheckListItemViewSet, self).create(request, *args, **kw)

    def list(self, request):
        return Response(
                data={
                    'detail': 'Action not permitted',
                    },
                status=403,
                )

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(
                    data={
                        'detail': 'Authentication required',
                        },
                    status=403,
                    )
        check_list_item = CheckListItem.objects.get(id=pk)

        perms = get_perms(
                user_or_group=request.user,
                obj=check_list_item.check_list,
                )

        if 'view_checklist' not in perms:
            return Response(
                    data={
                        'detail': 'Permission denied',
                        },
                    status=403,
                    )

        serializer = self.serializer_class(check_list_item)

        return Response(
                data=serializer.data,
                status=200,
                )


class CheckListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CheckList model
    """
    allowed_methods = ['GET', 'POST', ]
    filter_backends = (DjangoObjectPermissionsFilter, )
    model = CheckList
    permission_classes = (JotterObjectPermissions, )
    serializer_class = CheckListSerializer

    def pre_save(self, obj):
        """
        Actions to perform before saving a CheckList
        """
        obj.owner = self.request.user

    def post_save(self, obj, created=False):
        """
        Actions to perform immediately after saving a CheckList
        """
        if created:
            assign_perm('api.change_checklist', obj.owner, obj)
            assign_perm('api.delete_checklist', obj.owner, obj)
            assign_perm('api.view_checklist', obj.owner, obj)


class GroupViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the Group model
    '''
    model = Group


class SessionViewSet(viewsets.ViewSet):
    """
    Session handler view
    """
    permission_classes = []

    @method_decorator(ensure_csrf_cookie)
    def create(self, request):
        """
        Create a new session

        effectively logs in a user
        """
        required_params = ['password', 'username', ]
        for param in required_params:
            if param not in request.DATA:
                return Response(
                        status=400,
                        data={
                            'detail': 'Parameter required: %s' % param,
                            },
                        )

        username = request.DATA.get('username', '')
        password = request.DATA.get('password', '')
        user = authenticate(username=username, password=password, )
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(
                        status=201,
                        data={
                            'detail': 'Authentication successful',
                            'isAuthenticated': request.user.is_authenticated(),
                            'username': request.user.username,
                            },
                        )
            else:
                return Response(
                        status=400,
                        data={
                            'detail': 'Inactive user',
                            },
                        )
        else:
            return Response(
                    status=400,
                    data={
                        'detail': 'Invalid username or password',
                        },
                    )
    def delete(self, request):
        """
        Delete a user's session

        effectively logs out the current user
        """
        if request.user.is_authenticated():
            logout(request)
            return Response(
                    status=204,
                    data={
                        'detail': 'User logged out',
                        'isAuthenticated': request.user.is_authenticated(),
                        'username': request.user.username,
                        },
                    )
        else:
            return Response(
                    status=400,
                    data={
                        'detail': 'No session found',
                        },
                    )

    def list(self, request):
        """
        Return session info
        """
        return Response(
                status=200,
                data={
                    'detail': 'Session found',
                    'isAuthenticated': request.user.is_authenticated(),
                    'username': request.user.username,
                    },
                )


class UpdateCodebaseViewSet(viewsets.ViewSet):
    """
    Update the project's codebase
    """
    permission_classes = []
    def create(self, request):
        """
        Handle a POST request and run the update script
        """
        jotter_root = os.path.realpath(os.path.join(
            settings.PROJECT_PATH,
            '../../',
            ))
        subprocess.Popen(
                '/usr/bin/sudo {jotter_root}/bin/update.sh'.format(
                    jotter_root=jotter_root,
                    ),
                shell=True,
                )

        # Touch the wsgi file to restart the process
        try:
            os.utime('{jotter_root}/server/server/wsgi.py'.format(
                jotter_root=jotter_root,
                ),
                None,
                )
        except:
            pass

        return Response(
                data={
                    'detail': 'Codebase updated',
                    },
                status=200,
                )


class UserViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for the User model
    '''
    model = User
