from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from event.models import Product
from team.models import Team
from sponsor.models import RICSponsor
from .models import About,Gallery
from members.models import RICEvent
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import View


from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView



# # Create your views here.
def event_analytics(request):
    labels = []
    values = []

    # Get the number of events for each institute
    events_by_institute = RICEvent.objects.values('event').annotate(total=Count('event'))

    # Create labels and values lists for the chart
    for event in events_by_institute:
        labels.append(event['event'])
        values.append(event['total'])

    # Create a dictionary containing the data to be returned as JSON
    data = {
        'labels': labels,
        'values': values
    }

    return JsonResponse(data)

class EventAnalyticsView(TemplateView):
    template_name = 'home/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = RICEvent.objects.exclude(event__isnull=True).values('event').annotate(total=Count('id')).order_by('-total')
        labels = [d['event'] for d in data]
        values = [d['total'] for d in data]
        context['labels'] = labels
        context['values'] = values
        return context

class GalleryView(ListView):
    model = Gallery
    template_name = 'home/gallery.html'
    context_object_name = 'images'

# def GalleryView(request):
#     return render(request,'home/gallery.html')


class LoginView(TemplateView):
    template_name = "home/test.html"

class AboutList(ListView):
    model = About
    template_name='home/about.html'


class ProductListView(ListView):
    model = Product
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['team_list'] = Team.objects.all()
        context['about_list'] = About.objects.all()
        context['sponsor_list'] = RICSponsor.objects.all().order_by('order')
        return context