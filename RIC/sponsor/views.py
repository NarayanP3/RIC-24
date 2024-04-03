from django.shortcuts import render
from django.views.generic import TemplateView,ListView, CreateView,FormView
from .models import Sponsor, RICSponsor, SponsorReg
from .forms import SponsorRegForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

class SponsorListView(ListView):
    model = Sponsor
    template_name = "sponsor/list.html"

    def get_context_data(self, **kwargs):
        context = super(SponsorListView, self).get_context_data(**kwargs)
        context['oursponsor_list'] = RICSponsor.objects.all()
        return context


class SponsorRegView(FormView):
    template_name = "sponsor/sponsor_reg.html"
    form_class = SponsorRegForm
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

from django.shortcuts import render
from django.views.generic import TemplateView

class SponsorRegSuccessView(TemplateView):
    template_name = "sponsor/sponsor_reg_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['alert'] = self.request.GET.get('alert')
        return context