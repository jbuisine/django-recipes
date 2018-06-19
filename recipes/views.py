from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from recipes.forms import CustomUserCreationForm, RecipeForm, CommentForm, ImageForm, VideoForm
from recipes.models import Recipe, RecipeComment, RecipeImage
from django.shortcuts import redirect


# constants
NUMBER_OF_RECIPES_PER_PAGE = 1
NUMBER_OF_COMMENTS_PER_PAGE = 1


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
        raise Http404("Recipe does not exist")

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

            # TODO : use of specific redirect
            return redirect('recipes:media-manage', recipe_id=recipe_obj.id)
    else:
        recipe_form = RecipeForm()

    return render(request, 'recipes/user/add_recipe.html', {'recipe_form': recipe_form})


@login_required()
def recipe_manage(request, recipe_id):

    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    if request.user != recipe.user:
        raise HttpResponseForbidden("You cannot update this recipe")

    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)
        video_form = VideoForm(request.POST)
        if image_form.is_valid():
            new_file = RecipeImage(image=request.FILES['file'], recipe= recipe)
            new_file.save()
    else:
        video_form = VideoForm()
        image_form = ImageForm()

    return render(request, 'recipes/user/manage_recipe.html', {'image_form': image_form, 'recipe': recipe})


@login_required()
def recipe_media_upload(request, recipe_id):
    try:
        recipe_id = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    uploaded_file = request.FILES['file']
    print(request.FILES)
    RecipeImage.objects.create(recipe=recipe_id, image=uploaded_file)

    return JsonResponse({'success': "yes"})
