'''
Jotter url paterns
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from api.views import CheckListViewSet, CheckListItemViewSet, GroupViewSet, \
        SessionViewSet, UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'check-lists', CheckListViewSet)
router_v1.register(r'check-list-items', CheckListItemViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'sessions', SessionViewSet, base_name='sessions')
router_v1.register(r'users', UserViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include(router_v1.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls',
        namespace='rest_framework')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
)
