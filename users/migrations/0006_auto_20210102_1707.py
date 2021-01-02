# Generated by Django 3.1.4 on 2021-01-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210102_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='athleteuser',
            name='height',
            field=models.FloatField(default=0, help_text='Hieght of the user in Cm', verbose_name='height'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athleteuser',
            name='born_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='athleteuser',
            name='weight',
            field=models.FloatField(help_text='Weight of the user in Kg', verbose_name='weight'),
        ),
    ]
