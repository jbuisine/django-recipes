from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect

from recipes.models import Recipe
from recipes.views import NUMBER_OF_RECIPES_PER_PAGE
from recipes.views import recipe_query_search
# Create your views here.
from users.forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':

        signup_form = CustomUserCreationForm(request.POST, request.FILES)

        if signup_form.is_valid():
            signup_form.save()

            return redirect('recipes:home')
    else:
        signup_form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'signup_form': signup_form})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


@login_required()
def account(request):
    # getting recipes of user

    recipes = Recipe.objects.with_annotates().filter(user=request.user).all()

    mean_of_marks_user = 0
    if recipes.count() != 0:
        mean_of_marks_user = sum([recipe.mean_of_marks for recipe in recipes]) / recipes.count()

    return render(request, 'users/account.html', {'mean_of_marks_user': mean_of_marks_user})


@login_required()
def user_recipes(request):
    # getting recipes of user

    query = request.GET.get('search', "")

    recipes = recipe_query_search(query, None)

    recipes_list = recipes.filter(user=request.user).order_by('-published_at')
    paginator = Paginator(recipes_list, NUMBER_OF_RECIPES_PER_PAGE)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'users/user_recipes.html', {'recipes': recipes})


def user_detail(request, user_username_slug):
    try:
        selected_user = User.objects.get(username=user_username_slug)
    except Recipe.DoesNotExist:
        raise Http404("User does not exist")

    recipes = Recipe.objects.with_annotates().filter(user=selected_user).all()

    mean_of_marks_user = 0
    if recipes.count() != 0:
        mean_of_marks_user = sum([recipe.mean_of_marks for recipe in recipes]) / recipes.count()

    return render(request, 'users/show_profile.html',
                  {'selected_user': selected_user, 'mean_of_marks_user': mean_of_marks_user})
