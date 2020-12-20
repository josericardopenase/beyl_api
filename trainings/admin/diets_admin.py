from django.contrib import admin
from ..models.diets import *
import nested_admin

#Diet, DietDay, DietGroup, DietFood
# Register your models here.
class DietFoodAdmin(nested_admin.NestedStackedInline):
    model = DietFood
    extra = 0

class DietGroupAdmin(nested_admin.NestedStackedInline):
    inlines = [DietFoodAdmin, ]
    model = DietGroup
    extra = 0

class DietDayAdmin(nested_admin.NestedStackedInline):
    inlines = [DietGroupAdmin, ]
    model = DietDay
    sortable_field_name="order"
    extra = 0

class DietAdmin(nested_admin.NestedModelAdmin):
    inlines = [DietDayAdmin, ]

admin.site.register(Diet, DietAdmin)
admin.site.register(Food)