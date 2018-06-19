from django.contrib import admin

from recipes.models import Ingredient, IngredientUnitMeasure, \
                           IngredientFamily, IngredientPhoto, \
                           RecipeType, RecipeDifficulty


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
    list_display = ['label', 'level']
    ordering = ['level']
    actions_on_bottom = True


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ['name', 'family']

    # custom tabular inline for many to many relationship
    class IngredientUnitMeasureInline(admin.TabularInline):
        model = Ingredient.unit_measure.through
        extra = 1

    class IngredientPhotoInline(admin.StackedInline):
        model = IngredientPhoto

    inlines = [
        IngredientUnitMeasureInline,
        IngredientPhotoInline
    ]

    # exclude unit_measure because it will be used into inlines
    exclude = ('unit_measure',)
