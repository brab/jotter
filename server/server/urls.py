from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from api.views import GroupViewSet, UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'users', UserViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^api/v1/', include(router_v1.urls)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls',
        namespace='rest_framework')),
)
