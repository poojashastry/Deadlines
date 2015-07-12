__author__ = 'Pooja'

# imports
from . import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<name>[a-z]+)/$', views.usernames, name='usernames'),
]