from django.contrib import admin
from .models import Bio,RICEvent,IC, ICEvent, Event1,Event2,Dept,Subdomain,Workshop,WorkshopBio,Accommodation,IntegrationBee,MathEvent,MathEventIndividual,DifferentiaChallenge, ProblemState,Hackathon
from import_export.admin import ImportExportModelAdmin
from .custom_filters import DuplicatVideoFilter

# Register your models here.
class FilterAdmin(ImportExportModelAdmin):
    list_display = ("__str__",'name','email','institute',"dept","abstract","razorpay_payment_id")
    list_filter = (DuplicatVideoFilter,"dept","event1","institute","iitg_student")
    search_fields = ('name','email','institute',)

class FilterDept(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class FilterEvent(ImportExportModelAdmin):
    list_display = ("name","fee",'deadline')
    search_fields = ("name","fee",'deadline')

class FilterICEvent(ImportExportModelAdmin):
    list_display = ("name","fee",'deadline')
    search_fields = ("name","fee",'deadline')

class FilterRICAdmin(ImportExportModelAdmin):
    list_display = ("__str__",'name','email','institute',"dept","abstract","razorpay_payment_id")
    list_filter = ("dept","event","institute","iitg_student")
    search_fields = ('name','email','institute',)


class FilterICAdmin(ImportExportModelAdmin):
    list_display = ("__str__",'name','email','institute',"razorpay_payment_id")
    list_filter = ("event","institute","iitg_student")
    search_fields = ('institute','name','email',)

class FilterAdminInt(ImportExportModelAdmin):
    list_display = ("__str__",'unique_id','school_college_name',"class_name","number")
    search_fields = ('class_name',)

class FilterAdminD(ImportExportModelAdmin):
    list_display = ("__str__",'unique_id','school_college_name',"class_name","number")
    search_fields = ('class_name',)

class FilterAdminMOI(ImportExportModelAdmin):
    list_display = ("__str__",'unique_id','school_name',"class_name","number")
    list_filter = ("class_name",'school_name')
    search_fields = ('class_name','school_name',)

class FilterAdminMO(ImportExportModelAdmin):
    list_display = ("__str__",'unique_id','school_name',"school_contact","student_list","teacher_list")
    search_fields = ('school_name',)

class WorkshopAdmin(ImportExportModelAdmin):
    list_display = ('__str__', 'dept', 'razorpay_payment_id', 'email', 'name')
    list_filter = ("workshop",)

admin.site.register(RICEvent,FilterRICAdmin)
admin.site.register(IC,FilterICAdmin)
admin.site.register(ICEvent,FilterICEvent)
admin.site.register(Event1,FilterEvent)
admin.site.register(Event2,FilterEvent)
admin.site.register(Dept,FilterDept)
admin.site.register(Workshop)
admin.site.register(WorkshopBio,WorkshopAdmin)
admin.site.register(Accommodation)
admin.site.register(IntegrationBee,FilterAdminInt)
admin.site.register(ProblemState)
admin.site.register(Hackathon)
