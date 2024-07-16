from django.shortcuts import render
from .models import Product,Speaker,DeptSpeaker
from members.models import Workshop
from django.views.generic import TemplateView,ListView, DetailView, CreateView, UpdateView,DeleteView
from django.shortcuts import get_object_or_404
# Create your views here.

class ProductDetail(DetailView):
    model = Product
    template_name='event/detail.html'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name').upper().replace('-', ' ')
        return get_object_or_404(Product, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workshop_list"] = Workshop.objects.all()
        context['event'] = self.object
        return context


class SpeakerDetailView(DetailView):
    model = Speaker
    template_name='event/institutespeakerdetail.html'


class DeptSpeakerListView(ListView):
    model = Speaker
    template_name = "event/speaker.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["speaker_list"] = Speaker.objects.all()
        context["dept_speaker_list"] = DeptSpeaker.objects.all()
        return context


class DeptSpeakerDetailView(DetailView):
    model = DeptSpeaker
    template_name='event/institutespeakerdetail.html'

def merchandise_view(request):
    return render(request, 'event/merchandise.html')