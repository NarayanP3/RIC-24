from django.contrib import admin
from .models import Cat, Sponsor,RICSponsor,SponsorReg
# Register your models here.
admin.site.register(Cat)
admin.site.register(Sponsor)
admin.site.register(SponsorReg)
admin.site.register(RICSponsor)


