# Generated by Django 3.1.7 on 2021-03-25 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20210208_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generalhistory',
            options={'ordering': ('-date',)},
        ),
    ]