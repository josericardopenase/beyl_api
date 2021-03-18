from django.contrib import admin
from ..models.rutine import *
import nested_admin

#Rutine, RutineDay, RutineGRoup, RutineExcersise
# Register your models here.
class RutineExcersise(nested_admin.NestedStackedInline):
    model = RutineExcersise
    extra = 0

class RutineGroup(nested_admin.NestedStackedInline):
    inlines = [RutineExcersise, ]
    model = RutineGroup
    extra = 0

class RutineDayAdmin(nested_admin.NestedStackedInline):
    inlines = [RutineGroup, ]
    model = RutineDay
    sortable_field_name="order"
    extra = 0

class RutineAdmin(nested_admin.NestedModelAdmin):
    inlines = [RutineDayAdmin, ]

class ExcersiseAdmin(admin.ModelAdmin):
    model = Excersise
    list_filter = ('muscles',)
    search_fields = ('name', 'muscles')
    list_display = ('name', 'muscles')

admin.site.register(Rutine, RutineAdmin)
admin.site.register(Excersise, ExcersiseAdmin)