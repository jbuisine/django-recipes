from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
import requests
from django.forms import NumberInput
from django.utils.translation import ugettext_lazy as _
from recipes.models import Profile, Recipe, RecipeComment, RecipeMark, RecipeImage, RecipeVideo, \
    RecipeIngredient, IngredientUnitMeasure, IngredientFamily, Ingredient, RecipeStep


class RecipeForm(forms.ModelForm):
    """
        Recipe form utilization
    """

    class Meta:
        model = Recipe
        exclude = ['user', 'members', 'number_of_marks', 'mean_of_marks', 'recipe_ingredients', 'slug', 'published']

        prepation_time = forms.IntegerField(label=_('Preparation time in minutes'))
        cooking_time = forms.IntegerField(label=_('Cooking time in minutes'))
        relaxation_time = forms.IntegerField(label=_('Relaxation time in minutes'))

        # define widgets of time field
        widgets = {
            'preparation_time': NumberInput(attrs={'min': 0}),
            'cooking_time': NumberInput(attrs={'min': 0}),
            'relaxation_time': NumberInput(attrs={'min': 0}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(label= _('Enter your comment'),
                              widget=forms.Textarea(attrs={'placeholder': _('Comment'), 'rows': 2}))

    class Meta:
        model = RecipeComment
        fields = ['content']


class MediaForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = RecipeImage()
        exclude = ['recipe', 'path']

    def __init__(self, *args, **kwargs):
        self.image = kwargs.pop('image', None)
        super(MediaForm, self).__init__(*args, **kwargs)


class ImageForm(forms.Form):
    image = forms.ImageField()

    class Meta:
        model = RecipeImage
        fields = ('image',)


class VideoForm(forms.ModelForm):
    path = forms.URLField(label=_('link of your video'))

    class Meta:
        model = RecipeVideo
        fields = ('path',)


class MarkForm(forms.ModelForm):
    class Meta:
        model = RecipeMark
        exclude = ['created_at', 'user']


class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        exclude = ['recipe', 'level']


def fill_ingredient_families():
    """
    Function created to avoid issue when filling choices of RecipeIngredientForm
    when database is not already created

    :return: all choices of ingredients families
    """
    families_choices = [('', '-----------')]

    for family in IngredientFamily.objects.all():
        families_choices.append((family.id, family.name))

    return list(families_choices)


class RecipeIngredientForm(forms.ModelForm):

    # use of specific function to fill this choice field
    ingredient_families = forms.ChoiceField(label=_('Choose the ingredient family'),
                                            choices=fill_ingredient_families,
                                            required=True)

    class Meta:
        model = RecipeIngredient
        fields = (
            'ingredient_families',
            'ingredient',
            'quantity',
            'unit_measure',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.none()
        self.fields['unit_measure'].queryset = IngredientUnitMeasure.objects.none()

        if 'ingredient_families' in self.data:
            try:
                ingredient_family_id = int(self.data.get('ingredient_families'))
                self.fields['ingredient'].queryset = Ingredient.objects.filter(family_id=ingredient_family_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Ingredient queryset
        elif self.instance.pk:
            self.fields['ingredient'].queryset = self.instance.ingredient_families.ingredient_set.order_by('name')

        if 'ingredient' in self.data:
            try:
                ingredient_id = int(self.data.get('ingredient'))
                ingredient = Ingredient.objects.get(id=ingredient_id)
                units = IngredientUnitMeasure.objects.filter(ingredient=ingredient).order_by('name')
                self.fields['unit_measure'].queryset = units
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Unit queryset
        elif self.instance.pk:
            self.fields['unit_measure'].queryset = self.instance.ingredient.unit_measure_set.order_by('name')


class CustomUserCreationForm(forms.ModelForm):

    """
        Custom UserCreationForm using Profile class
    """

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'date_of_birth',
            'country_choice',
            'avatar',
        )
        exclude = ['country', 'county_flag']

        widgets = {
            'avatar': forms.ClearableFileInput()
        }

    first_name = forms.CharField(label=_('Enter your firstname '),
                                 widget=forms.TextInput(attrs={'placeholder': 'Firstname'}),
                                 min_length=4,
                                 max_length=150,
                                 required=True)

    last_name = forms.CharField(label=_('Enter your lastname '),
                                widget=forms.TextInput(attrs={'placeholder': 'Lastname'}),
                                min_length=4,
                                max_length=150,
                                required=True)

    username = forms.CharField(label=_('Enter Username'),
                               min_length=4,
                               max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}),
                               required=True)

    email = forms.EmailField(label=_('Enter email'),
                             widget=forms.TextInput(attrs={'placeholder': 'example@recipes.com'}),
                             required=True)

    password1 = forms.CharField(label=_('Enter password'),
                                widget=forms.PasswordInput(attrs={'placeholder': ''}),
                                min_length=8,
                                required=True)

    password2 = forms.CharField(label=_('Confirm password'),
                                widget=forms.PasswordInput(attrs={'placeholder': ''}),
                                min_length=8,
                                required=True)

    date_of_birth = forms.DateField(label=_('Date of birth'),
                                    required=True,
                                    widget=forms.SelectDateWidget(years=range(1900, datetime.date.today().year + 1)))

    # getting country from resp api
    country_api_url = 'https://restcountries.eu/rest/v2/all'
    country_data = requests.get(url=country_api_url).json()

    country_choice = forms.ChoiceField(label=_('Your country'),
                                       choices=[(idx, val['name']) for idx, val in enumerate(country_data)],
                                       required=True)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError(_("Username already exists"))
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError(_("Email already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Password don't match"))

        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return last_name

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])

        # retrieve country index from form
        country_index = int(self.cleaned_data['country_choice'])

        # create specific Profile for this user
        user_profile = Profile()
        user_profile.user = user
        user_profile.avatar = self.cleaned_data['avatar']
        user_profile.date_of_birth = self.cleaned_data['date_of_birth']
        user_profile.country = self.country_data[country_index]['name']
        user_profile.country_flag = self.country_data[country_index]['flag']
        user_profile.save()

        return user
