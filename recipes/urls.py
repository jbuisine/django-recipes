from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]