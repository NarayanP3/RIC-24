from django.contrib import admin
from .models import Product,Speaker,DeptSpeaker
# Register your models here.
admin.site.register(Product)
admin.site.register(Speaker)
admin.site.register(DeptSpeaker)
