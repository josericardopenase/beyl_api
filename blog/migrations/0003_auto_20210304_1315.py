# Generated by Django 3.1.7 on 2021-03-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210110_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='texto',
            field=models.TextField(),
        ),
    ]