# Generated by Django 3.1.4 on 2021-01-10 20:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='texto',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
