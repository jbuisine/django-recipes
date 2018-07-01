# Generated by Django 2.0.4 on 2018-06-28 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20180628_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipestep',
            name='level',
        ),
        migrations.AlterField(
            model_name='recipestep',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipes.Recipe'),
        ),
    ]
