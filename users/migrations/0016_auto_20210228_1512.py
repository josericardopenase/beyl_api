# Generated by Django 3.1.7 on 2021-02-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210216_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='profile.png', upload_to='', verbose_name='Profile_pic'),
        ),
    ]