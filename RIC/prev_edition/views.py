from django.shortcuts import render

from django.views.generic.base import TemplateView  
# Create your views here.
class RC18(TemplateView):
    template_name = 'prev_edition/rc18.html'

class RC19(TemplateView):
    template_name = 'prev_edition/rc19.html'

class RC20(TemplateView):
    template_name = 'prev_edition/rc20.html'