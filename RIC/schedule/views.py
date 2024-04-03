from django.shortcuts import render
from django.views.generic import TemplateView,ListView
# Create your views here.
from home.models import About


class ScheduleView(ListView):
    model = About
    template_name = "schedule/list.html"


    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['about_list'] = About.objects.all()
        return context
