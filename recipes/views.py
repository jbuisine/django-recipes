from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from recipes.forms import CustomUserCreationForm, RecipeForm
from recipes.models import Recipe


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
