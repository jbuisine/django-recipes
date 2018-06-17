from django.urls import path
from django.contrib.auth import views as auth_views

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.show_recipes, name='home'),

    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),

    path('recipes/add', views.add_recipe, name='add_recipe'),
]