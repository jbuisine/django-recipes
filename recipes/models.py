from datetime import date, datetime

# import of User auth django model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.utils.text import slugify


# useful function to set dynamic directory path to save file
def avatar_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/user_<id>/<filename>
    return 'media/avatars/{0}/{1}'.format(self.user.id, filename)


class Profile(models.Model):
    """
        Custom attributes for user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_path, default='media/avatars/default_avatar.png')
    date_of_birth = models.DateField()
    country = models.CharField(max_length=255)
    country_flag = models.TextField(default='')

    def __str__(self):
        return "Profile of %s " % self.user.username

    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - \
               ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class IngredientUnitMeasure(models.Model):
    """
       Specify a unit measure
    """
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.label)


class IngredientFamily(models.Model):
    """
       Specify a family name of Ingredient
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
       Represents an ingredient
    """
    name = models.CharField(max_length=255)
    family = models.ForeignKey(IngredientFamily, on_delete=models.CASCADE)
    unit_measure = models.ManyToManyField(IngredientUnitMeasure)

    def __str__(self):
        return self.name


class IngredientPhoto(models.Model):
    """
        Photo of an ingredient
    """
    path = models.ImageField(upload_to='media/ingredients/')
    created_at = models.DateTimeField(auto_now_add=True)
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='photo')

    def __str__(self):
        return "Photo of %s : %s" % (self.ingredient, self.path)


###############
# Recipe part #
###############

class RecipeDifficulty(models.Model):
    """
        Difficulty of recipe could be :
            - Very easy, Easy, Medium, Hard and so on..
            - or a score ?
    """
    label = models.CharField(max_length=255)
    level = models.IntegerField(default=0)

    class Meta:
        ordering = ['level']

    def __str__(self):
        return "Level %s : %s" % (self.level, self.label)


class RecipeType(models.Model):
    """
        Specify the type of recipe
    """
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class RecipeManager(models.Manager):
    """
        Custom manager : query to get aggregate annotations fields
    """

    def with_annotates(self):
        return super(RecipeManager, self).get_queryset() \
            .annotate(number_of_marks=Coalesce(Count('marks'), 0)) \
            .annotate(mean_of_marks=Coalesce(Avg('marks__mark_score'), 0))


class Recipe(models.Model):
    """
         Representation of recipe
             - associated with difficulty
             - associated to a type of recipe
             - can be created, updated and deleted by an user
     """
    objects = RecipeManager()

    # description fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField()
    realization_cost = models.FloatField(default=0, validators=[MinValueValidator(0)])
    published = models.BooleanField(default=False)

    # time fields (use of integer field by default : number of minutes)
    preparation_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cooking_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    relaxation_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    recipe_number_person = models.IntegerField(default=1)

    # date information fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # check to update when step or description are added
    published_at = models.DateTimeField(auto_now=True)

    # foreign key fields
    recipe_difficulty = models.ForeignKey(RecipeDifficulty, on_delete=models.CASCADE)
    recipe_types = models.ManyToManyField(RecipeType, related_name='recipe')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    # many to many fields
    recipe_ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='ingredients')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Recipe, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()


class RecipeIngredient(models.Model):
    """
        Link a recipe and an ingredient with specific quantity
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.FloatField(default=0)

    # In form get specific unit from ingredient units
    unit_measure = models.ForeignKey(IngredientUnitMeasure, on_delete=models.PROTECT)

    def __str__(self):
        return "Recipe %s includes %s %s of %s " % (self.recipe, self.quantity,
                                                    self.unit_measure, self.ingredient)


class RecipeStep(models.Model):
    """
        Specify a step of how to do recipe
    """
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='steps')

    def __str__(self):
        return "Step : %s" % self.description


class RecipeVideo(models.Model):
    path = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='videos')


# useful function to set dynamic directory path to save file
def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/%Y/%m/%d/<filename>
    current_date = datetime.today().strftime('%Y/%m/%d')
    return 'media/user_{0}/{1}/{2}'.format(self.recipe.user.id, current_date, filename)


class RecipeImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='images')


class RecipeComment(models.Model):
    """
        Comment of recipe
    """
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)


class RecipeMark(models.Model):
    """
        Mark given by a user for a recipe
    """
    mark_score = models.FloatField(default=0., validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='marks')

    def __str__(self):
        return "%s, give a mark %s to %s at %s" % (self.user.username, self.mark_score,
                                                   self.recipe.title, self.created_at)


class Notification(models.Model):
    """
        Notification class for comment or mark of recipe
        User will be notify each time anyone else comment or mark his recipe
    """
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(RecipeComment, on_delete=models.PROTECT, default=None)
    mark = models.ForeignKey(RecipeMark, on_delete=models.PROTECT, default=None)

    def __str__(self):

        if self.comment:
            return self.comment

        elif self.mark:
            return self.mark
