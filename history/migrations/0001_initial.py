# Generated by Django 3.1.4 on 2021-01-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementSportsHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='Modified at')),
                ('history_type', models.CharField(choices=[('WEIGHT', 'weight'), ('HEIGHT', 'height'), ('FAT', 'fat')], max_length=100, verbose_name='Type of history behaviour')),
                ('data', models.FloatField(verbose_name='Weight historial')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SportHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='Modified at')),
                ('name', models.CharField(max_length=30, verbose_name='Name of the excersise')),
                ('date', models.DateField(verbose_name='Date of the excersise')),
                ('time', models.TimeField()),
                ('has_distance', models.BooleanField()),
                ('distance', models.FloatField(blank=True)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]