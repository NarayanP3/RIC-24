from django.contrib import admin
from .models import Team,Dept,Position,Cat
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class FilterAdmin(ImportExportModelAdmin):
    list_display = ('name','position')
    list_filter = ("name","position")



# Register your models here.
admin.site.register(Team,FilterAdmin)
admin.site.register(Dept)
admin.site.register(Position)
admin.site.register(Cat)
