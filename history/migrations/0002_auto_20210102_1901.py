# Generated by Django 3.1.4 on 2021-01-02 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurementsportshistory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='sporthistory',
            options={},
        ),
        migrations.AddField(
            model_name='measurementsportshistory',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date of the publication'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurementsportshistory',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sporthistory',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sporthistory',
            name='date',
            field=models.DateField(verbose_name='Date of the publication'),
        ),
    ]
