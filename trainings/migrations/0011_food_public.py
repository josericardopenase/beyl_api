# Generated by Django 3.1.7 on 2021-03-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0010_auto_20210228_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='public',
            field=models.BooleanField(db_column='is_public', default=False),
        ),
    ]
