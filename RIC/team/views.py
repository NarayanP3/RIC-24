from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import Team
# Create your views here.



class TeamListView(ListView):
    model = Team
    template_name = "team/list.html"
    ordering = ['order']