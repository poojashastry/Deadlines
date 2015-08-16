__author__ = 'Pooja'

# imports
from . import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<first_name>[a-z]+)/$', views.usernames, name='usernames'),
    url(r'^user/login/$', views.login_page, name='login_page'),
    url(r'^user/auth/$', views.login_view, name='login_view'),
    url(r'^user/logout/$', views.logout_view, name='logout'),
    url(r'^user/register/$', views.register, name='register'),
    url(r'^user/signup/$', views.signup, name='signup'),
    url(r'^user/createProject/$', views.createProject, name='createProject'),
    url(r'^user/addProject/$', views.addProject, name='addProject'),
    url(r'^user/(?P<projectName>[A-Za-z]+)/$', views.projectDetails, name='projectDetails')
]