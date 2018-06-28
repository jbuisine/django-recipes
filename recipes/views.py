from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from recipes.forms import CustomUserCreationForm, RecipeForm, CommentForm, ImageForm, VideoForm, RecipeIngredientForm, \
    MarkForm, RecipeStepForm

from django.db.models import Q

from recipes.models import Recipe, RecipeComment, RecipeImage, RecipeIngredient, Ingredient, IngredientFamily, \
    IngredientUnitMeasure, RecipeVideo, RecipeStep

from django.shortcuts import redirect

import os

# constants
NUMBER_OF_RECIPES_PER_PAGE = 6
NUMBER_OF_COMMENTS_PER_PAGE = 6


def signup(request):
    if request.method == 'POST':

        signup_form = CustomUserCreationForm(request.POST, request.FILES)

        for key in request.FILES:
            print(key)

        if signup_form.is_valid():
            signup_form.save()

            return redirect('recipes:home')
    else:
        signup_form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'signup_form': signup_form})


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
    recipes_list = Recipe.objects.with_annotates().filter(published=True).order_by('-published_at')
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


def detail(request, recipe_slug):
    try:
        recipe = Recipe.objects.with_annotates().get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    comments_list = RecipeComment.objects.all().filter(recipe=recipe).order_by('-created_at')

    paginator = Paginator(comments_list, NUMBER_OF_COMMENTS_PER_PAGE)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    # get current mark of user if exists
    current_mark_score = 0

    mark = recipe.marks.all().filter(user=request.user).first()

    if mark:
        current_mark_score = mark.mark_score

    if request.method == 'POST':

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            obj.user = request.user
            obj.recipe = recipe
            obj.save()

            # init new comment form if comment saved
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'recipes/detail_recipe.html',
                  context={'recipe': recipe,
                           'comments': comments,
                           'current_mark_score': current_mark_score,
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

            return redirect('recipes:recipe-manage', recipe_slug=recipe_obj.slug)
    else:
        recipe_form = RecipeForm()

    return render(request, 'recipes/user/add_recipe.html', {'recipe_form': recipe_form})


@login_required()
def manage_recipe(request, recipe_slug):
    try:
        recipe = Recipe.objects.with_annotates().get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    if request.user != recipe.user:
        raise HttpResponseForbidden("You cannot update this recipe")

    if request.method == 'POST':
        ingredient_form = RecipeIngredientForm(request.POST)
        step_form = RecipeStepForm(request.POST)

        if ingredient_form.is_valid():
            recipe_ingredient_obj = ingredient_form.save(commit=False)
            recipe_ingredient_obj.recipe = recipe
            recipe_ingredient_obj.save()

        if step_form.is_valid():
            step_obj = step_form.save(commit=False)

            step_count = RecipeStep.objects.filter(recipe=recipe).count()

            step_obj.level = step_count + 1
            step_obj.recipe = recipe
            step_obj.save()

    else:
        ingredient_form = RecipeIngredientForm()
        step_form = RecipeStepForm()

    try:
        video = RecipeVideo.objects.get(recipe=recipe)
        video_form = VideoForm(instance=video)
    except RecipeVideo.DoesNotExist:
        video_form = VideoForm(request.POST)

    return render(request, 'recipes/user/manage_recipe.html',
                  {'video_form': video_form,
                   'ingredient_form': ingredient_form,
                   'step_form': step_form,
                   'recipe': recipe})


@login_required()
def recipe_video_upload(request,recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    video_form = VideoForm(request.POST)
    if video_form.is_valid():
        try:
            video = RecipeVideo.objects.get(recipe=recipe)
            video.path = request.POST.get('path')
            video.save()
        except RecipeVideo.DoesNotExist:
            video = RecipeVideo.objects.create(recipe=recipe,path=request.POST.get('path'))
            video.save()

    return redirect('recipes:recipe-manage', recipe_slug=recipe_slug)


@login_required()
def recipe_media_upload(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    for key in request.FILES:
        RecipeImage.objects.create(recipe=recipe, image=request.FILES[key])

    return JsonResponse({'newfilename': ""})


@login_required()
def recipe_media_delete(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    image = request.GET.get('img', None)

    try :
        RecipeImage.objects.get(image=image, recipe=recipe).delete()
        os.remove(image)
        pass
    except RecipeImage.DoesNotExist:
        current_date = datetime.today().strftime('%Y/%m/%d')
        file_path = 'static/media/user_'+str(recipe.user.id)+'/'+current_date+'/'+image
        RecipeImage.objects.get(image=file_path, recipe=recipe).delete()
        os.remove(file_path)

    return JsonResponse({'success': True})


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

    return render(request, 'recipes/partials/recipes/forms/_recipe_ingredient_select.html',
                  {'ingredients': ingredients})


@login_required()
def get_units_of_ingredient(request):
    ingredient_id = request.GET.get('ingredient_id')

    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Recipe.DoesNotExist:
        raise Http404("Ingredient does not exist")

    # get all ingredients
    units_measure = IngredientUnitMeasure.objects.all().filter(ingredient=ingredient)

    return render(request, 'recipes/partials/recipes/forms/_ingredient_units_select.html',
                  {'units_measure': units_measure})


@login_required()
def delete_recipe_ingredient(request, recipe_ingredient_id):
    try:
        recipe_ingredient = RecipeIngredient.objects.get(id=recipe_ingredient_id)
    except Recipe.DoesNotExist:
        raise Http404("Ingredient family does not exist")

    recipe_slug = recipe_ingredient.recipe.slug

    # remove recipe ingredient
    recipe_ingredient.delete()

    return redirect('recipes:recipe-manage', recipe_slug=recipe_slug)


###############
# Marks parts #
###############
def add_or_update_mark(request):

    if request.method == 'POST':
        # get mark form
        mark_form = MarkForm(request.POST)

        if mark_form.is_valid():
            mark_obj = mark_form.save(commit=False)

            # getting recipe object from form
            mark_obj.user = request.user

            # retrieve recipe
            recipe = mark_obj.recipe

            mark_obj_exists = recipe.marks.all().filter(user=request.user).first()

            # mark already exists
            if mark_obj_exists:
                # update mark
                mark_obj_exists.mark_score = mark_obj.mark_score
                mark_obj_exists.save()
            else:
                mark_obj.save()

            # TODO : find another way to reload annotate (if exists)
            # get new recipe aggregate values
            recipe = Recipe.objects.with_annotates().get(id=recipe.id)

            return JsonResponse({'recipe_mark_mean': recipe.mean_of_marks,
                                 'number_of_marks': recipe.number_of_marks})


@login_required()
def delete_recipe_step(request, step_id):
    try:
        recipe_step = RecipeStep.objects.get(id=step_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe step does not exist")

    recipe_slug = recipe_step.recipe.slug

    # remove recipe step
    recipe_step.delete()

    return redirect('recipes:recipe-manage', recipe_slug=recipe_slug)


def search(request):
    query = request.GET.get('search')
    recipes_list = Recipe.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(recipes_list, NUMBER_OF_RECIPES_PER_PAGE)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/show_recipes.html', {'recipes': recipes})

