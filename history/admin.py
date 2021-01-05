from django.contrib import admin
from .models import WeightHistory, GeneralHistory

# Register your models here.

class WeightHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'data', 'add_date')

class GeneralHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time',  'has_distance')

admin.site.register(WeightHistory, WeightHistoryAdmin)
admin.site.register(GeneralHistory, GeneralHistoryAdmin)
