# Generated by Django 2.0.4 on 2018-06-19 18:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0007_auto_20180619_1801'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageRecipe',
            new_name='RecipeImage',
        ),
        migrations.RenameModel(
            old_name='VideoRecipe',
            new_name='RecipeVideo',
        ),
        migrations.RenameModel(old_name='Comment', new_name='RecipeComment'),
        migrations.RenameModel(old_name='Mark', new_name='RecipeMark'),
    ]
