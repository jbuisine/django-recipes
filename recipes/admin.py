from django.contrib import admin

from recipes.models import MediaType, IngredientUnitMeasure, IngredientFamily, Ingredient, \
                           RecipeType, RecipeDifficulty


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ['label']
    actions_on_bottom = True


@admin.register(IngredientUnitMeasure)
class IngredientUnitMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'label']
    actions_on_bottom = True


@admin.register(IngredientFamily)
class IngredientFamilyAdmin(admin.ModelAdmin):
    list_display = ['name']
    actions_on_bottom = True


@admin.register(RecipeType)
class RecipeTypeAdmin(admin.ModelAdmin):
    list_display = ['label']
    actions_on_bottom = True


@admin.register(RecipeDifficulty)
class RecipeDifficultyAdmin(admin.ModelAdmin):
    list_display = ['label']
    actions_on_bottom = True


@admin.register(Ingredient)
class RecipeDifficultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'family', 'unit_measure']
    actions_on_bottom = True
