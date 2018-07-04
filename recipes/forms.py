from django import forms
from django.forms import NumberInput
from django.utils.translation import ugettext_lazy as _

from recipes.models import Recipe, RecipeComment, RecipeMark, RecipeImage, RecipeVideo, \
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
            'unit_measure',
            'quantity',
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