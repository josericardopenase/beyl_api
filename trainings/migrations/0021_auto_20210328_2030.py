# Generated by Django 3.1.7 on 2021-03-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0020_auto_20210328_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='public',
            field=models.BooleanField(blank=True, db_column='is_public', default=False, null=True),
        ),
    ]
