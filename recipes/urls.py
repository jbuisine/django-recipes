from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.show_recipes, name='home'),

    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    re_path(r'^recipe/(?P<recipe_id>\d+)/$', views.detail, name='detail'),
    re_path(r'^recipe/media/(?P<recipe_id>\d+)/$', views.media_manage, name='media-manage'),
    re_path(r'^recipe/media/(?P<recipe_id>\d+)/upload-ajax$', views.uploadImage_ajax, name='image-upload-ajax'),
    path('recipes/add', views.add_recipe, name='add_recipe'),
]