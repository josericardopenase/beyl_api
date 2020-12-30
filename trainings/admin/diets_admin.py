from django.contrib import admin
from ..models.diet import *
import nested_admin

#Diet, DietDay, DietGroup, DietFood
# Register your models here.
class DietRecipeFoodAdmin(nested_admin.NestedStackedInline):
    model = DietRecipeFood
    extra = 0

class DietRecipeAdmin(nested_admin.NestedStackedInline):
    inlines = [DietRecipeFoodAdmin, ]
    model = DietRecipe
    extra = 0

class DietFoodAdmin(nested_admin.NestedStackedInline):
    model = DietFood
    extra = 0

class DietGroupAdmin(nested_admin.NestedStackedInline):
    inlines = [DietFoodAdmin, DietRecipeAdmin ]
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