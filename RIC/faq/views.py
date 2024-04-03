from django.shortcuts import render
from .models import FAQ
from django.views.generic import TemplateView,ListView
from .filters import FAQFilter
# Create your views here.
class FAQList(ListView):
    model = FAQ
    template_name='faq/list.html'

    # def get_queryset(self):
    #     return FAQ.objects.filter().order_by("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FAQFilter(self.request.GET, queryset=self.get_queryset())
        return context