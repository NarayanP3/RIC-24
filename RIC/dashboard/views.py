import json
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Event1,Event2,Bio,RICEvent, IC, ICEvent,WorkshopBio,IntegrationBee,MathEvent, MathEventIndividual,DifferentiaChallenge,Accommodation
from .forms import BioForm,RICForm,ICForm ,AbstractForm,AbstractICForm,AbstractRICForm,WorkshopForm,AccommodationForm,IntegrationBeeForm,MathEventForm, MathEventIndividualForm,IDForm, StudDetailForm,DifferentiaChallengeForm

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.

import pandas as pd
import pdfkit
import os
from django.db.models import Count
from django.contrib.auth import get_user_model


# Create your views here.

def send_instructions(request):
    if request.user.is_superuser:
        int_part = IntegrationBee.objects.all()


        recipient_list = []

        # get all the registered users

        # for participant in int_part:
        #     recipient_list.append(participant.owner.email)



        cc_list1 = [
                "c.chetan@iitg.ac.in",
                'a.hitesh@iitg.ac.in',
                's.narayan@iitg.ac.in',
                'p.rishi@iitg.ac.in',
                'shubham.energy@iitg.ac.in',
                'nikhil1996@iitg.ac.in',

            ]


        email_from = settings.EMAIL_HOST_USER
        bcc_list = list(set(recipient_list))  # remove duplicates
        cc_list = list(set(cc_list1))  # remove duplicates
        subject = "Details about Integration BEE | RIC'24"
        context = {'subject': subject}
        html_template = 'dashboard/instruction_mail.html'
        html_message = render_to_string(html_template, context=context)

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=email_from,
            cc=cc_list,
            bcc=bcc_list,
            reply_to=[email_from],
        )
        message.content_subtype = 'html'
        message.send()

        return redirect('members:all')


    return redirect('members:all')
