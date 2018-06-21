from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from recipes.forms import CustomUserCreationForm, RecipeForm, CommentForm, ImageForm, VideoForm, RecipeIngredientForm

from recipes.models import Recipe, RecipeComment, RecipeImage, RecipeIngredient, Ingredient, IngredientFamily, \
    IngredientUnitMeasure

from django.shortcuts import redirect

import os

# constants
NUMBER_OF_RECIPES_PER_PAGE = 6
NUMBER_OF_COMMENTS_PER_PAGE = 6


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('recipes:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'recipes/index.html')


@login_required()
def account(request):

    # getting recipes of user
    recipes_list = Recipe.objects.all().filter(published=True, user=request.user).order_by('-published_at')
    paginator = Paginator(recipes_list, NUMBER_OF_RECIPES_PER_PAGE)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/user/account.html', {'recipes': recipes})


def show_recipes(request):
    recipes_list = Recipe.objects.all().filter(published=True).order_by('-published_at')
    paginator = Paginator(recipes_list, NUMBER_OF_RECIPES_PER_PAGE)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/show_recipes.html', {'recipes': recipes})


def user_detail(request, user_username):

    try:
        selected_user = User.objects.get(username=user_username)
    except Recipe.DoesNotExist:
        raise Http404("User does not exist")

    return render(request, 'recipes/show_profile.html', {'selected_user': selected_user})


def detail(request, recipe_id):
    try:
        recipe_id = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    comments_list = RecipeComment.objects.all().filter(recipe=recipe_id).order_by('-created_at')

    paginator = Paginator(comments_list, NUMBER_OF_COMMENTS_PER_PAGE)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    if request.method == 'POST':

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            obj.user = request.user
            obj.recipe = recipe_id
            obj.save()

            # init new comment form if comment saved
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'recipes/detail_recipe.html',
                  context={'recipe': recipe_id,
                           'comments': comments,
                           'comment_form': comment_form})


@login_required()
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():
            # getting recipe object from form
            recipe_obj = recipe_form.save(commit=False)
            recipe_obj.user = request.user
            recipe_obj.save()

            return redirect('recipes:recipe-manage', recipe_id=recipe_obj.id)
    else:
        recipe_form = RecipeForm()

    return render(request, 'recipes/user/add_recipe.html', {'recipe_form': recipe_form})


@login_required()
def manage_recipe(request, recipe_id):

    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    if request.user != recipe.user:
        raise HttpResponseForbidden("You cannot update this recipe")

    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)
        video_form = VideoForm(request.POST)
        ingredient_form = RecipeIngredientForm(request.POST)

        if image_form.is_valid():
            new_file = RecipeImage(image=request.FILES['file'], recipe=recipe)
            new_file.save()

        if ingredient_form.is_valid():
            recipe_ingredient_obj = ingredient_form.save(commit=False)
            recipe_ingredient_obj.recipe = recipe
            recipe_ingredient_obj.save()

    else:
        video_form = VideoForm()
        image_form = ImageForm()
        ingredient_form = RecipeIngredientForm()

    return render(request, 'recipes/user/manage_recipe.html',
                  {'image_form': image_form,
                   'video_form': video_form,
                   'ingredient_form': ingredient_form,
                   'recipe': recipe})


@login_required()
def recipe_media_upload(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    for key in request.FILES:
        RecipeImage.objects.create(recipe=recipe, image=request.FILES[key])

    return JsonResponse({'newfilename': ""})


@login_required()
def recipe_media_delete(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    image = request.GET.get('img', None)
    os.remove(image)
    RecipeImage.objects.get(image=image, recipe=recipe).delete()

    return JsonResponse({'success': "delete"})


#####################
# Ingredients parts #
#####################

@login_required()
def get_ingredients_of_family(request):

    ingredient_family_id = request.GET.get('ingredient_family')

    try:
        ingredient_family = IngredientFamily.objects.get(id=ingredient_family_id)
    except Recipe.DoesNotExist:
        raise Http404("Ingredient family does not exist")

    # get all ingredients
    ingredients = Ingredient.objects.all().filter(family=ingredient_family).values()

    return render(request, 'recipes/partials/recipes/forms/_recipe_ingredient_select.html', {'ingredients': ingredients})


@login_required()
def get_units_of_ingredient(request):

    ingredient_id = request.GET.get('ingredient_id')

    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Recipe.DoesNotExist:
        raise Http404("Ingredient does not exist")

    # get all ingredients
    units_measure = IngredientUnitMeasure.objects.all().filter(ingredient=ingredient)

    return render(request, 'recipes/partials/recipes/forms/_ingredient_units_select.html', {'units_measure': units_measure})


@login_required()
def delete_recipe_ingredient(request, recipe_ingredient_id):

    try:
        recipe_ingredient = RecipeIngredient.objects.get(id=recipe_ingredient_id)
    except Recipe.DoesNotExist:
        raise Http404("Ingredient family does not exist")

    recipe_id = recipe_ingredient.recipe.id

    # remove recipe ingredient
    recipe_ingredient.delete()

    return redirect('recipes:recipe-manage', recipe_id=recipe_id)
