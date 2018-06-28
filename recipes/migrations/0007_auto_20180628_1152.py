# Generated by Django 2.0.4 on 2018-06-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20180628_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_type',
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_types',
            field=models.ManyToManyField(to='recipes.RecipeType'),
        ),
    ]