# Generated by Django 2.0.4 on 2018-06-26 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20180624_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_number_person',
            field=models.IntegerField(default=1),
        ),
    ]