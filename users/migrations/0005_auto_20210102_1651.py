# Generated by Django 3.1.4 on 2021-01-02 16:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0005_excersise_video'),
        ('users', '0004_auto_20201231_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='athleteuser',
            name='alergias',
            field=models.ManyToManyField(to='trainings.Food'),
        ),
        migrations.AddField(
            model_name='athleteuser',
            name='born_date',
            field=models.DateField(default=datetime.datetime(2021, 1, 2, 16, 51, 37, 304726, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='athleteuser',
            name='fat',
            field=models.FloatField(default=10, help_text='Fat in percentage', verbose_name='fat_percent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='athleteuser',
            name='sexo',
            field=models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer'), ('O', 'Otro')], default='M', help_text='Choices of sex', max_length=8, verbose_name='sex_choices'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='athleteuser',
            name='weight',
            field=models.FloatField(default=70, help_text='Weight of the user', verbose_name='weight'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]