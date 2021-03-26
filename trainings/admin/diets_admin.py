from django.contrib import admin
from ..models.diet import *
import nested_admin
from django.db.models.functions import Lower
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

class FoodAdmin(admin.ModelAdmin):
    model = Food
    list_filter = ('name',)
    search_fields = ('name',)
    list_display = ('name', 'kcalories',  'carbohydrates', 'protein' ,'fat', )
    ordering = [Lower('name')]


admin.site.register(FoodTag)
admin.site.register(Diet, DietAdmin)
admin.site.register(Food, FoodAdmin)