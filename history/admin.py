from django.contrib import admin
from .models import MeasurementHistory, SportHistory

# Register your models here.
admin.site.register(MeasurementHistory)
admin.site.register(SportHistory)
