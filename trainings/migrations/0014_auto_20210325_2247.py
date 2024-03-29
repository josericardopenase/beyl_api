# Generated by Django 3.1.7 on 2021-03-25 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0013_auto_20210325_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excersise',
            name='tags',
            field=models.ManyToManyField(blank=True, db_table='trainings_excersise_tags', to='trainings.ExcersiseTag'),
        ),
        migrations.AlterField(
            model_name='food',
            name='tags',
            field=models.ManyToManyField(blank=True, db_table='trainings_food_tags', to='trainings.FoodTag'),
        ),
    ]
