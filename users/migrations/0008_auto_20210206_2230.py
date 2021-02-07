# Generated by Django 3.1.4 on 2021-02-06 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210128_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleteuser',
            name='sexo',
            field=models.CharField(choices=[('hombre', 'H'), ('mujer', 'M')], help_text='Choices of sex', max_length=8, verbose_name='sex_choices'),
        ),
    ]
