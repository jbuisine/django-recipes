from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from recipes.forms import CustomUserCreationForm, RecipeForm, CommentForm
from recipes.models import Recipe, Comment


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
    recipes = Recipe.objects.all()
    return render(request, 'recipes/show_recipes.html', {'recipes': recipes})

def recipe_detail(request,id):

    try:
        recipe_id =Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    feedback = Comment.objects.all().filter(recipe=recipe_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.recipe = recipe_id
            obj.save()
    else:
        form = CommentForm()

    return render(request, 'recipes/detail_recipe.html', context={'recipe':recipe_id,'feedback':feedback,'form':form})


@login_required()
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            # TODO : use of specific redirect
            return HttpResponseRedirect('/')
    else:
        form = RecipeForm()

    return render(request, 'recipes/user/add_recipe.html', {'form': form})
