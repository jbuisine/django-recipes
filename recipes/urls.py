from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    # home page
    path('', views.show_recipes, name='home'),
    path('type/<int:type_id>', views.show_recipes_by_type, name='home-type'),
    path('difficulty/<int:difficulty_id>', views.show_recipes_by_difficulty, name='home-difficulty'),

    # recipe part
    path('recipes/add', views.add_or_update_recipe, name='recipe-add-or-update'),
    path('recipe/publish', views.publish_recipe, name='recipe-publish-state'),
    path('recipe/<slug:recipe_slug>/', views.detail, name='recipe-detail'),
    path('recipe/manage/<slug:recipe_slug>/', views.manage_recipe, name='recipe-manage'),
    path('recipe/<slug:recipe_slug>/delete/', views.recipe_delete, name='recipe-delete'),
    path('recipe/update/<int:recipe_id>/', views.recipe_update, name='recipe-update'),

    # recipe media part
    path('recipe/manage/media/<slug:recipe_slug>/upload', views.recipe_media_upload, name='recipe-media-upload'),
    path('recipe/manage/media/<slug:recipe_slug>/delete', views.recipe_media_delete, name='recipe-media-delete'),
    path('recipe/manage/media/<slug:recipe_slug>/upload-video', views.recipe_video_upload, name='recipe-video-upload'),

    # recipe ingredient part
    path('recipe/ingredients-of-family', views.get_ingredients_of_family, name='recipe-ingredients-of-family'),
    path('recipe/unit-of-ingredient', views.get_units_of_ingredient, name='recipe-unit-of-ingredient'),
    path('recipe/delete-recipe-ingredient/<int:recipe_ingredient_id>/', views.delete_recipe_ingredient,
         name='recipe-delete-ingredient'),
    path('recipe/update-recipe-ingredient', views.update_recipe_ingredient, name='recipe-update-ingredient'),

    # mark part
    path('recipe/add-or-update-mark', views.add_or_update_mark, name='recipe-add-or-update-mark'),

    # recipe step part
    path('recipe/delete-step/<int:step_id>/', views.delete_recipe_step, name='recipe-delete-step'),
    path('recipe/update-step', views.update_recipe_step, name='recipe-update-step'),

]
