from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.show_recipes, name='home'),

    # user part
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    re_path(r'^profile/(?P<user_username>\w+)/$', views.user_detail, name='user-detail'),

    # recipe part
    path('recipes/add', views.add_recipe, name='add_recipe'),
    re_path(r'^recipe/(?P<recipe_id>\d+)/$', views.detail, name='recipe-detail'),
    re_path(r'^recipe/manage/(?P<recipe_id>\d+)/$', views.manage_recipe, name='recipe-manage'),
    re_path(r'^recipe/manage/media/(?P<recipe_id>\d+)/upload$', views.recipe_media_upload, name='recipe-media-upload'),
    re_path(r'^recipe/manage/media/(?P<recipe_id>\d+)/delete$', views.recipe_media_delete, name='recipe-media-delete'),

    re_path('recipe/ingredients-of-family', views.get_ingredients_of_family, name='recipe-ingredients-of-family'),
    re_path('recipe/unit-of-ingredient', views.get_units_of_ingredient, name='recipe-unit-of-ingredient'),
    re_path(r'^recipe/delete-recipe-ingredient/(?P<recipe_ingredient_id>\d+)/$', views.delete_recipe_ingredient, name='recipe-delete-ingredient')
]