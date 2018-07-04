from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = [
    # user part
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    path('profile/<slug:user_username_slug>/', views.user_detail, name='user-detail'),
    path('password/', views.change_password, name='change-password'),
    path('recipes/', views.user_recipes, name='user-recipes'),
]
