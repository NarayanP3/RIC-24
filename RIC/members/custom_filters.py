from django.contrib.admin import SimpleListFilter

class DuplicatVideoFilter(SimpleListFilter):
    title = 'Unique'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return (('unique', 'Unique'),)

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'unique':
            return queryset.filter().exclude(id__in=[name.id for name in queryset.distinct().order_by("email")])
