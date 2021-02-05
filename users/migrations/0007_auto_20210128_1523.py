# Generated by Django 3.1.4 on 2021-01-28 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0006_auto_20210102_1804'),
        ('users', '0006_auto_20210102_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='athleteuser',
            name='trainer_diet',
            field=models.OneToOneField(blank=True, help_text='Diet of the user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_diet', to='trainings.diet'),
        ),
        migrations.AddField(
            model_name='athleteuser',
            name='trainer_rutine',
            field=models.OneToOneField(blank=True, help_text='Rutine of the user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_rutine', to='trainings.rutine'),
        ),
        migrations.DeleteModel(
            name='Invitation',
        ),
    ]
