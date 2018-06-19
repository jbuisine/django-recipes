from django.db import models

# import of User auth django model
from django.contrib.auth.models import User
from datetime import date, datetime


class Profile(models.Model):
    """
        Custom attributes for user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField()
    date_of_birth = models.DateField()
    country = models.CharField(max_length=255)
    country_flag = models.TextField(default='')

    def __str__(self):
        return "Profile of %s " % self.user.username

    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - \
               ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class IngredientFamily(models.Model):
    """
       Specify a family name of Ingredient
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IngredientUnitMeasure(models.Model):
    """
       Specify a unit measure
    """
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.label)


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
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)

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

    def __str__(self):
        return "Level %s : %s" % (self.level, self.label)


class RecipeType(models.Model):
    """
        Specify the type of recipe
    """
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Recipe(models.Model):
    """
         Representation of recipe
             - associated with difficulty
             - associated to a type of recipe
             - can be created, updated and deleted by an user
     """
    # description fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    realization_cost = models.FloatField()
    published = models.BooleanField(default=False)

    # time fields
    preparation_time = models.DurationField()
    cooking_time = models.DurationField()
    relaxation_time = models.DurationField(default=0)

    # mark fields
    mean_of_marks = models.FloatField(default=0.)
    number_of_marks = models.IntegerField(default=0)

    # date information fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # check to update when step or description are added
    published_at = models.DateTimeField(auto_now=True)

    # foreign key fields
    recipe_difficulty = models.ForeignKey(RecipeDifficulty, on_delete=models.CASCADE)
    recipe_type = models.ForeignKey(RecipeType, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # many to many fields
    members = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.title

    def add_mark(self, mark):
        # compute the value of mean
        self.mean_of_marks = self.mean_of_marks * self.number_of_marks + mark / self.number_of_marks + 1
        # increase number of mark
        self.number_of_marks += 1
        # save model
        self.save()


class RecipeIngredient(models.Model):
    """
        Link a recipe and an ingredient with specific quantity
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    # In form get specific unit from ingredient units
    unit_measure = models.ForeignKey(IngredientUnitMeasure, on_delete=models.CASCADE)

    def __str__(self):
        return "Recipe %s includes %s %s of %s " % (self.recipe, self.quantity,
                                                    self.unit_measure,  self.ingredient)


class RecipeStep(models.Model):
    """
        Specify a step of how to do recipe
    """
    level = models.IntegerField()
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return "Step %s  : %s" % (self.level, self.description)


class RecipeVideo(models.Model):
    path = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='videos')


# useful function to set dynamic directory path to save file
def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/%Y/%m/%d/<filename>
    current_date = datetime.today().strftime('%Y/%m/%d')
    return 'static/media/user_{0}/{1}/{2}'.format(self.recipe.user.id, current_date, filename)


class RecipeImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')


class RecipeComment(models.Model):
    """
        Comment of recipe
    """
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeMark(models.Model):
    """
        Mark given by a user for a recipe
    """
    mark_score = models.FloatField(default=0.)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

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
    comment = models.ForeignKey(RecipeComment, on_delete=models.CASCADE, default=None)
    mark = models.ForeignKey(RecipeMark, on_delete=models.CASCADE, default=None)

    def __str__(self):

        if self.comment:
            return self.comment

        elif self.mark:
            return self.mark
