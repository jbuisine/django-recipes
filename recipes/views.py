from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from recipes.forms import CustomUserCreationForm, RecipeForm, CommentForm, MediaForm
from recipes.models import Recipe, Comment

# constants
NUMBER_OF_RECIPES_PER_PAGE = 1


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # TODO : use of specific redirect
            return HttpResponseRedirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'recipes/index.html')


@login_required()
def account(request):
    return render(request, 'recipes/user/account.html')


def show_recipes(request):
    recipes_list = Recipe.objects.all().filter(published=True).order_by('-published_at')
    paginator = Paginator(recipes_list, NUMBER_OF_RECIPES_PER_PAGE)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/show_recipes.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    try:
        recipe_id = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    feedback = Comment.objects.all().filter(recipe=recipe_id).order_by('-created_at')

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
                  context={'recipe': recipe_id, 'feedback': feedback, 'comment_form': comment_form})


@login_required()
def add_recipe(request):
    if request.method == 'POST':
        media_form = MediaForm(request.POST)
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid() and media_form.is_valid():
            # getting recipe object from form
            recipe_obj = recipe_form.save(commit=False)
            recipe_obj.user = request.user
            recipe_obj.save()

            # getting new recipe media object and link it to recipe
            media_obj = media_form.save(commit=False)
            media_obj.recipe = recipe_obj
            media_obj.save()

            # TODO : use of specific redirect
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm()
        media_form = MediaForm()

    return render(request, 'recipes/user/add_recipe.html', {'recipe_form': recipe_form, 'media_form': media_form})
