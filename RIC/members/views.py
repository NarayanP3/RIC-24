import json
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Event1,Event2,Bio,RICEvent, IC, ICEvent,WorkshopBio,IntegrationBee,MathEvent, MathEventIndividual,DifferentiaChallenge,Accommodation
from .forms import BioForm,RICForm,ICForm ,AbstractForm,AbstractICForm,AbstractRICForm,WorkshopForm,AccommodationForm,IntegrationBeeForm,MathEventForm, MathEventIndividualForm,IDForm, StudDetailForm,DifferentiaChallengeForm
import razorpay
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


def send_workshop(request):
    tt = "AI for All: Bootcamp"
    bio_participants = WorkshopBio.objects.filter(workshop__title=tt)
    if not bio_participants:
        return HttpResponse("Emails Not found")

    messages = []
    for participant in bio_participants:

        email = participant.owner.email
        username = participant.owner.username
        events = tt
        msg = events
        name = participant.name
        time = "14 May, 2023 03:00 PM to 06:00 PM"
        venue = "5G3, Classroom Complex"

        subject = "Workshop Information for RIC'23"
        context = {'subject': subject,'name':name,'events':events,'username':username,'venue':venue,'time':time,}
        html_template = 'workshop_mail.html'
        html_message = render_to_string(html_template, context=context)

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],

            cc=["c.chetan@iitg.ac.in","ihussain@iitg.ac.in","dprangan@iitg.ac.in","k.kalpana@iitg.ac.in","v.bhargava@iitg.ac.in","hiteshiit4@gmail.com",],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        message.content_subtype = 'html'
        messages.append(message)


    count = len(messages)
    if count > 0:
        connection = get_connection()
        sent = connection.send_messages(messages)
        connection.close()
        return HttpResponse(f"Emails sent: {sent}/{count}")
        # return HttpResponse(f"Emails sent: {count} {msg}")
    else:
        return HttpResponse("No emails to send.")



def send_payment_empre(request):
    bio_participants = IC.objects.filter(event__name='EMPRENDIMIENTO')
    if not bio_participants:
        return HttpResponse("Emails Not found")

    messages = []
    for participant in bio_participants:

        email = participant.owner.email
        username = participant.owner.username
        events = participant.event
        name = participant.owner.username
        role = participant.role
        fee = participant.total/100

        subject = "Payment Information for RIC'23"
        context = {'subject': subject,'name':name,'events':events,'username':username,'role':role,'fee':fee,}
        html_template = 'payment_mail.html'
        html_message = render_to_string(html_template, context=context)

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            cc=["c.chetan@iitg.ac.in",],
            # cc=["c.chetan@iitg.ac.in","ihussain@iitg.ac.in","dprangan@iitg.ac.in","k.kalpana@iitg.ac.in","v.bhargava@iitg.ac.in","hiteshiit4@gmail.com",],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        message.content_subtype = 'html'
        messages.append(message)


    count = len(messages)
    if count > 0:
        connection = get_connection()
        sent = connection.send_messages(messages)
        connection.close()
        return HttpResponse(f"Emails sent: {sent}/{count}")
    else:
        return HttpResponse("No emails to send.")



def update_ic_fees(request):
    # Filter participants with "EMPRENDIMIENTO" event
    participants = IC.objects.filter(event__name="EMPRENDIMIENTO")

    # Update fees for each participant
    for participant in participants:
        participant.total = 50000  # Update fee to 1000 (or whatever value you want)
        participant.save()

    return HttpResponse(f"Fees updated for {len(participants)} participants.")



def registrations_count(request):
    events = Event1.objects.all()
    counts = {}
    for event in events:
        ric_reg = RICEvent.objects.filter(event=event).distinct('email')
        counts[event.name] = ric_reg.count()

    return render(request, 'members/registrations_count.html', {'counts': counts})

def update_workshop_bio(request):
    bios = WorkshopBio.objects.all()
    ics = IC.objects.all()
    counts = 0
    for bio in bios:
        users = User.objects.filter(email=bio.owner.email)
        if users.exists():
            user = users.first()
            bio.email = user.email
            bio.name = user.get_full_name()
            bio.save()
            counts +=1
    iccounts = 0
    for bio in ics:
        users = User.objects.filter(email=bio.owner.email)
        if users.exists():
            user = users.first()
            bio.email = user.email
            bio.name = user.get_full_name()
            bio.save()
            iccounts +=1
    # return render(request, 'members/registrations_count.html', {'counts': counts})
    return HttpResponse(request,f"Fees updated for {counts} and ic {iccounts}")

User = get_user_model()

def update_names_and_emails(request):
    events = RICEvent.objects.all()
    count = 0
    for event in events:
        count+=1
        owner = User.objects.get(id=event.owner_id)
        if event.name == 'Name':
            event.name = owner.get_full_name()
            event.email = owner.email
        event.save()
    return HttpResponse("Names and emails updated successfully"+str(count))


def update_bio_events(request):
    status = False
    bios = Bio.objects.all()
    status_bio =  False
    status_ric = False
    run = False
    ric_count = 0
    bio_count = 0

    for bio in bios:
        status = True
        events = bio.event1.all()
        run = True
        bio_count += 1

        for event in events:
            # Check if the event has already been added to RICEvent
            ric_count += 1
            # if not ric_bio.ricevent_set.filter(event=event).exists():
            # Calculate the fee based on the role of the participant
            if bio.role == "Student":
                fee = event.fee
            elif bio.role == "Academician":
                fee = 3 * event.fee
            elif bio.role == "Industry Expert":
                fee = 6 * event.fee
            else:
                fee = 6 * event.fee

            # Create a new RICEvent entry
            ric_event = RICEvent(
                institute=bio.institute,
                dept=bio.dept,
                abstract=bio.abstract,
                abstractFormat=bio.abstractFormat,
                event=event,
                number=bio.number,
                role=bio.role,
                owner=bio.owner,
                text=bio.text,
                total=fee,
                selected=False,
                selected_oral=False,
                razorpay_payment_id=bio.razorpay_payment_id,
                iitg_student=bio.iitg_student,
                remarks=bio.remarks,
            )
            status_ric = True
            ric_event.save()

        status_bio = True
    return render(request, 'success.html', {'status':status,'bio_count':bio_count,'ric_count':ric_count,'run_status':run,'status_bio':status_bio,'status_ric':status_ric})


def send_institute_invitation(request):

    # Path to the files
    directory_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'institute-mail')
    excel_path = os.path.join(directory_path, 'file.xlsx')
    html_path = os.path.join(directory_path, 'institute-mail.html')

    # Load the data from the Excel file
    data = pd.read_excel(excel_path)

    # Loop through the data and generate a PDF for each row
    for index, row in data.iterrows():
        name = row['Name']
        to_email = row['Email']

        # create mail content
        mail_content = render_to_string(html_path, {'name': name})


        # Attach the PDF to the email
        subject = "Invitation for Research and Industrial Conclave Integration'23"
        email_from = settings.EMAIL_HOST_USER
        email = EmailMessage(
                subject=subject,
                body=mail_content,
                from_email=email_from,
                to = [to_email],
                bcc=[email_from],
                reply_to=[email_from],
            )

        email.content_subtype = 'html'

        # Attach the brochure to the email
        brochure_path = os.path.join(directory_path, 'Brochure Final.pdf')
        with open(brochure_path, 'rb') as brochure_file:
            email.attach('Brochure Final.pdf', brochure_file.read(), 'application/pdf')

        # Send the email
        email.send()




    return render(request, 'success.html', {})


def send_speaker_invitation(request):
    # Path to the files
    directory_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'speaker-mail')
    excel_path = os.path.join(directory_path, 'file.xlsx')
    html_path = os.path.join(directory_path, 'speaker-mail.html')
    pdf_path = os.path.join(directory_path, 'Invitation letter.html')

    # Load the data from the Excel file
    data = pd.read_excel(excel_path)

    # Loop through the data and generate a PDF for each row
    for index, row in data.iterrows():
        name = row['Name']
        to_email = row['Email']
        # org = row['Organisation']

        # Render the HTML template with the data
        context = {'name': name}
        html_message = render_to_string(pdf_path, context=context)


        # Generate the PDF from the HTML template
        pdf_file = pdfkit.from_string(html_message, False)

        # create mail content
        mail_content = render_to_string(html_path, {'name': name})


        # Attach the PDF to the email
        subject = 'Invitation to Speak at Our Event'
        email_from = settings.EMAIL_HOST_USER
        email = EmailMessage(
                subject=subject,
                body=mail_content,
                from_email=email_from,
                to = [to_email],
                bcc=[email_from],
                reply_to=[email_from],
            )

        # message = EmailMessage(subject, 'Please see the attached invitation.', email_from, recipient_list)
        email.content_subtype = 'html'
        email.attach(f'{name}.pdf', pdf_file, 'application/pdf')

        # Attach the brochure to the email
        brochure_path = os.path.join(directory_path, 'Invitation letter.pdf')
        with open(brochure_path, 'rb') as brochure_file:
            email.attach('Invitation letter.pdf', brochure_file.read(), 'application/pdf')

        # Send the email
        email.send()

        # Delete the generated PDF file
        os.remove(f'{name}.pdf')

    return render(request, 'success.html', {})


def send_instructions(request):
    if request.user.is_superuser:
        int_part = IntegrationBee.objects.all()
        dsino_part = DifferentiaChallenge.objects.all()
        maths_part = MathEvent.objects.all()
        maths_indi_part = MathEventIndividual.objects.all()



        recipient_list = []

        for participant in int_part:
            recipient_list.append(participant.owner.email)

        for participant in dsino_part:
            recipient_list.append(participant.owner.email)
        recipient_list.append("chetan1gg1reigns@gmail.com")

        for participant in maths_part:
            recipient_list.append(participant.owner.email)

        for participant in maths_indi_part:
            recipient_list.append(participant.owner.email)



        cc_list1 = [
                "ihussain@iitg.ac.in",
                "v.bhargava@iitg.ac.in",
                "hiteshiit4@gmail.com",
                "c.chetan@iitg.ac.in"
            ]


        email_from = settings.EMAIL_HOST_USER
        bcc_list = list(set(recipient_list))  # remove duplicates
        cc_list = list(set(cc_list1))  # remove duplicates
        subject = "Details about D'sinoQuation"
        context = {'subject': subject}
        html_template = 'instruction_mail.html'
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


def send_mail_to_selected_participants(request):
    # bio_participants = RICEvent.objects.filter(selected=True,iitg_student=False)
    recipient_list = []
    cc_recipient_list = []
    counts = 0

    for participant in bio_participants:
        recipient_list.append(participant.owner.email)
    # for participant in ic_participants:
    #     recipient_list.append(participant.email)

    email_from = settings.EMAIL_HOST_USER
    bcc_list = list(set(recipient_list))  # remove duplicates
    cc_list = list(set(cc_recipient_list))  # remove duplicates
    subject = "[TRIAL MAIL] Payment Information for RIC'23"
    context = {'subject': subject}
    html_template = 'selected mail.html'
    html_message = render_to_string(html_template, context=context)

    counts = bcc_list.count()

    message = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=email_from,
        bcc=bcc_list,
        reply_to=[email_from],
    )
    message.content_subtype = 'html'
    message.send()

    return render('payment_mail.html')
    # return redirect('members:all')

from django.core.mail import EmailMultiAlternatives, get_connection


def send_payment(request):
    bio_participants = RICEvent.objects.filter(selected=True, iitg_student=False)
    if not bio_participants:
        return HttpResponse("Emails Not found")

    counts = bio_participants.count()



    messages = []
    for participant in bio_participants:
        email = participant.owner.email
        username = participant.owner.username
        events = participant.event
        name = participant.name
        role = participant.role
        fee = participant.total/100

        subject = "Payment Information for RIC'23"
        context = {'subject': subject,'name':name,'events':events,'username':username,'role':role,'fee':fee,}
        html_template = 'payment_mail.html'
        html_message = render_to_string(html_template, context=context)



        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            cc=["pratulkalita@iitg.ac.in","ihussain@iitg.ac.in","spal@iitg.ac.in","pankajk@iitg.ac.in","v.bhargava@iitg.ac.in","bpatel@iitg.ac.in","rubeka1995@iitg.ac.in"],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        message.content_subtype = 'html'
        messages.append(message)

    count = len(messages)
    if count > 0:
        connection = get_connection()
        sent = connection.send_messages(messages)
        connection.close()
        return HttpResponse(f"Emails sent: {sent}/{count}")
    else:
        return HttpResponse("No emails to send.")


def send_payment_workshop(request):
    bio_participants = WorkshopBio.objects.all()
    if not bio_participants:
        return HttpResponse("Emails Not found")


    messages = []
    for participant in bio_participants:
        email = participant.owner.email
        username = participant.owner.username
        workshops = participant.workshop.all()
        events = ', '.join([workshop.title for workshop in workshops])
        name = participant.name
        role = "Attendee"
        fee = participant.total/100

        subject = "Payment Information for RIC'23"
        context = {'subject': subject,'name':name,'events':events,'username':username,'role':role,'fee':fee,}
        html_template = 'payment_mail.html'
        html_message = render_to_string(html_template, context=context)

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            cc=["c.chetan@iitg.ac.in","ihussain@iitg.ac.in","dprangan@iitg.ac.in","k.kalpana@iitg.ac.in","v.bhargava@iitg.ac.in","hiteshiit4@gmail.com",],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        message.content_subtype = 'html'
        messages.append(message)

    count = len(messages)
    if count > 0:
        connection = get_connection()
        sent = connection.send_messages(messages)
        connection.close()
        return HttpResponse(f"Emails sent: {sent}/{count}")
    else:
        return HttpResponse("No emails to send.")



# def send_payment(request):
#     bio_participants = RICEvent.objects.filter(selected=True,iitg_student=False)
#     if not bio_participants:
#         return HttpResponse("Emails Not found")

#     counts = 0
#     recipient_list = []
#     cc_recipient_list = [
#                 "c.chetan@iitg.ac.in"
#                 ]

#     stre = ""

#     for participant in bio_participants:
#         counts += 1
#         email = participant.owner.email
#         username = participant.owner.username
#         events = participant.event
#         name = participant.name
#         role = participant.role
#         fee = participant.total/100

#         recipient_list.append(email)
#         stre += " "+email



#         email_from = settings.EMAIL_HOST_USER
#         bcc_list = list(set(recipient_list))  # remove duplicates
#         cc_list = list(set(cc_recipient_list))  # remove duplicates
#         subject = "[TRIAL MAIL] Payment Information for RIC'23"
#         context = {'subject': subject,'name':name,'events':events,'username':username,'role':role,'fee':fee,}
#         html_template = 'payment_mail.html'
#         html_message = render_to_string(html_template, context=context)

#         message = EmailMessage(
#             subject=subject,
#             body=html_message,
#             from_email=email_from,
#             bcc=email,
#             cc=cc_list,
#             reply_to=[email_from],
#         )
#         message.content_subtype = 'html'
#         message.send()

#     return HttpResponse("Emails"+str(stre)+" Counts"+str(counts))
#     # return render(request, 'payment_mail.html',{context=context})
#     # return redirect('members:all')

def change_all(request):
    MathEvent.objects.filter(selected=False).update(selected=True)
    MathEventIndividual.objects.filter(selected=False).update(selected=True)
    IntegrationBee.objects.filter(selected=False).update(selected=True)
    DifferentiaChallenge.objects.filter(selected=False).update(selected=True)

    return render(request, 'success.html', {})


class ProfileListView(LoginRequiredMixin, ListView):
    model = Bio
    template_name = "members/profile_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workshop_bio"] = WorkshopBio.objects.filter(owner = self.request.user)
        context["bio_list"] = Bio.objects.filter(owner = self.request.user)
        context["ric_list"] = RICEvent.objects.filter(owner = self.request.user)
        context["accommo"] = Accommodation.objects.filter(owner = self.request.user)
        context["intBee"] = IntegrationBee.objects.filter(owner = self.request.user)
        context["diffChall"] = DifferentiaChallenge.objects.filter(owner = self.request.user)
        context["mathEve"] = MathEvent.objects.filter(owner = self.request.user)
        context["mathEveInd"] = MathEventIndividual.objects.filter(owner = self.request.user)
        context["ic_list"] = IC.objects.filter(owner = self.request.user)

        return context


class ProfileCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = BioForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = BioForm()
        form.instance.owner = self.request.user
        title = "Research Events"
        context = {'title':title,'form':form}
        return context


    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()
        temp=0
        for i in form.instance.event1.all():
            if form.instance.role == "Student":
                temp=temp + i.fee
            elif form.instance.role == "Academician":
                temp=temp + 3*i.fee
            elif form.instance.role == "Industry Expert":
                temp=temp + 6*i.fee
            else:
                temp=temp + 6*i.fee
        print(temp)
        form.instance.total = temp
        form.save()

        user = self.request.user
        email = user.email
        username = user.username
        events = form.instance.event1.all()
        context = {'username': username,'email': email,'events':events}

        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        # return redirect("members:mail")


        return super().form_valid(form)


@method_decorator(csrf_exempt,name='dispatch')
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Bio
    template_name = "members/profile_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        context['rupee'] = self.object.total/100
        return context

    def post(self,request,*args,**kwargs):
        a = json.loads(request.body.decode('utf-8'))
        print(a['payment_id'])
        print(type(self.get_object()))
        self.get_object().setpaymentid(a['payment_id'])
        # self.get_object().save()
        print(self.get_object().razorpay_payment_id)
        return JsonResponse({
              "message":"Worked fine"
            })

def closed_view(request):
    return render(request, 'members/closed.html')

    # def get_success_url(self):
    #     return reverse('members:all')


class ProfileRICCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = RICForm
    template_name = 'members/profile_create.html'


    def get_context_data(self,*args, **kwargs):
        form = RICForm()
        form.instance.owner = self.request.user
        title = "Research Events"
        context = {'title':title,'form':form}
        return context


    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()

        temp=0



        selected_event = form.cleaned_data['event']
        if form.instance.role == "Student":
            temp = selected_event.fee
        elif form.instance.role == "Academician":
            temp = 3 * selected_event.fee
        elif form.instance.role == "Industry Expert":
            temp = 6 * selected_event.fee
        else:
            temp = 6 * selected_event.fee

        print(temp)
        form.instance.total = temp
        form.save()

        user = self.request.user
        email = user.email
        username = user.username
        events = form.instance.event
        context = {'username': username,'email': email,'events':events}

        user.save()
        html_template = 'mail_ric.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        # return redirect("members:mail")


        return super().form_valid(form)



@method_decorator(csrf_exempt,name='dispatch')
class ProfileRICDetailView(LoginRequiredMixin,DetailView):
    model = RICEvent
    template_name = "members/profile_detail_ric.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['rupee'] = self.object.total/100
        return context

    def post(self,request,*args,**kwargs):
        a = json.loads(request.body.decode('utf-8'))
        print(a['payment_id'])
        print(type(self.get_object()))
        self.get_object().setpaymentid(a['payment_id'])
        # self.get_object().save()
        print(self.get_object().razorpay_payment_id)
        return JsonResponse({
              "message":"Worked fine"
            })



class ProfileICCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = ICForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = ICForm()
        form.instance.owner = self.request.user
        title = "Industrial Events"
        context = {'title':title,'form':form}
        return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()


        # form.save_m2m()
        form.save()
        temp=0
        selected_event = form.cleaned_data['event']
        if form.instance.role == "Student":
            temp = selected_event.fee
        elif form.instance.role == "Academician":
            temp = 3 * selected_event.fee
        elif form.instance.role == "Industry Expert":
            temp = 6 * selected_event.fee
        else:
            temp = 6 * selected_event.fee

        form.instance.total = temp
        form.save()

        user = self.request.user
        email = user.email
        username = user.username
        events = form.instance.event
        context = {'username': username,'email': email,'events':events}

        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()

        return super().form_valid(form)

@method_decorator(csrf_exempt,name='dispatch')
class ProfileICDetailView(LoginRequiredMixin,DetailView):
    model = IC
    template_name = "members/profile_ic_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['rupee'] = self.object.total/100
        return context

    def post(self,request,*args,**kwargs):
        a = json.loads(request.body.decode('utf-8'))
        print(a['payment_id'])
        print(type(self.get_object()))
        self.get_object().setpaymentid(a['payment_id'])
        # self.get_object().save()
        print(self.get_object().razorpay_payment_id)
        return JsonResponse({
              "message":"Worked fine"
            })


class AbstractUpdateView(LoginRequiredMixin, View):
    template_name = 'members/update.html'
    success_url = reverse_lazy('members:all')
    def get(self, request, pk) :
        pic = get_object_or_404(Bio, id=pk, owner=self.request.user)
        form = AbstractForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(Bio, id=pk, owner=self.request.user)
        form = AbstractForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.abstractFormat =True
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)


class AbstractRICUpdateView(LoginRequiredMixin, View):
    template_name = 'members/update.html'
    success_url = reverse_lazy('members:all')
    def get(self, request, pk) :
        pic = get_object_or_404(RICEvent, id=pk, owner=self.request.user)
        form = AbstractRICForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(RICEvent, id=pk, owner=self.request.user)
        form = AbstractRICForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.abstractFormat =True
        pic.save()

        return redirect(self.success_url)


class AbstractICUpdateView(LoginRequiredMixin, View):
    template_name = 'members/update.html'
    success_url = reverse_lazy('members:all')
    def get(self, request, pk) :
        pic = get_object_or_404(IC, id=pk, owner=self.request.user)
        form = AbstractICForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(IC, id=pk, owner=self.request.user)
        form = AbstractICForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.icSubmissionFormat =True
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)


class WorkshopCreateView(LoginRequiredMixin,CreateView):
    form_class = WorkshopForm
    template_name = 'members/workshop_create.html'
    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()
        temp=0
        events = []

        for i in form.instance.workshop.all():
            temp=temp+i.fee
            events.append(i.title)
        form.instance.total = temp
        # return super().form_valid(form)

        response = super().form_valid(form)

        user = self.request.user
        user.save()
        email = user.email
        username = user.username
        # events = bios.all()
        # events = Event1.objects.all()
        # events = Bio.objects.all()
        context = {'username': username,'email': email,'events':events}
        # mydict = {'username': username}
        user.save()
        html_template = 'mail_work.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()

        return super().form_valid(form)

@method_decorator(csrf_exempt,name='dispatch')
class WorkshopDetailView(LoginRequiredMixin,DetailView):
    model = WorkshopBio
    template_name = "members/workshop_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['rupee'] = self.object.total/100
        return context

    def post(self,request,*args,**kwargs):
        a = json.loads(request.body.decode('utf-8'))
        print(a['payment_id'])
        print(type(self.get_object()))
        self.get_object().setpaymentid(a['payment_id'])
        # self.get_object().save()
        print(self.get_object().razorpay_payment_id)
        return JsonResponse({
              "message":"Worked fine"
            })


class AccommodationCreateView(LoginRequiredMixin, CreateView):
    login_required = True
    form_class = AccommodationForm
    template_name = 'members/accommodation_create.html'

    # def get_context_data(self,*args, **kwargs):
    #     form = AccommodationForm()
    #     form.instance.owner = self.request.user
    #     title = "Accommodation"
    #     context = {'title':title,'form':form}
    #     return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()

        user = self.request.user
        user.save()
        email = user.email
        username = user.username

        # form.instance.event_rc_list = Bio.objects.filter(owner=self.request.user)
        # form.instance.event_ic_list = ICEvent.objects.filter(owner=self.request.user)
        # form.save_m2m()

        # events = form.instance.events.all()
        events = form.instance.college
        context = {'username': username,'email': email,'events':events}
        # mydict = {'username': username}
        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()


        return super().form_valid(form)


@method_decorator(csrf_exempt,name='dispatch')
class AccommodationDetailView(LoginRequiredMixin,DetailView):
    model = Accommodation
    template_name = "members/accommodation_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['rupee'] = self.object.total/100


        self.object.event_rc_list = Bio.objects.filter(owner=self.request.user)
        self.object.event_ic_list = ICEvent.objects.filter(owner=self.request.user)


        return context

    def post(self,request,*args,**kwargs):
        a = json.loads(request.body.decode('utf-8'))
        print(a['payment_id'])
        print(type(self.get_object()))
        self.get_object().setpaymentid(a['payment_id'])
        # self.get_object().save()
        print(self.get_object().razorpay_payment_id)
        return JsonResponse({
              "message":"Worked fine"
            })


class IntegrationBeeCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = IntegrationBeeForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = IntegrationBeeForm()
        form.instance.owner = self.request.user
        title = "Integration BEE"
        context = {'title':title,'form':form}
        return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()


        user = self.request.user
        email = user.email
        username = user.username
        # bios = Bio.objects.filter(owner=user)
        title = "Integration Bee"
        events = [title]
        # events = bios.all()
        # events = Event1.objects.all()
        # events = Bio.objects.all()
        context = {'username': username,'email': email,'events':events,'title':title}
        # mydict = {'username': username}
        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        # return redirect("members:mail")
        return super().form_valid(form)


@method_decorator(csrf_exempt,name='dispatch')
class IntegrationBeeDetailView(LoginRequiredMixin,DetailView):
    model = IntegrationBee
    template_name = "members/integrationBee_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class DifferentiaChallengeCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = DifferentiaChallengeForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = DifferentiaChallengeForm()
        form.instance.owner = self.request.user
        title = "D'Sinoquation"
        context = {'title':title,'form':form}
        return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()
        # temp=0
        # # for i in form.instance.event1.all():
        # #     temp=temp+i.fee
        # print(temp)
        # temp=temp+form.instance.event2.fee
        # print(temp)
        # form.instance.total = self.request.fee

        user = self.request.user
        email = user.email
        username = user.username
        # bios = Bio.objects.filter(owner=user)
        title = "Differentia Challenge"
        events = [title]
        # events = bios.all()
        # events = Event1.objects.all()
        # events = Bio.objects.all()
        context = {'username': username,'email': email,'events':events,'title':title}
        # mydict = {'username': username}
        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        # return redirect("members:mail")
        return super().form_valid(form)


@method_decorator(csrf_exempt,name='dispatch')
class DifferentiaChallengeDetailView(LoginRequiredMixin,DetailView):
    model = DifferentiaChallenge
    template_name = "members/integrationBee_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class MathEventCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = MathEventForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = MathEventForm()
        form.instance.owner = self.request.user
        title = "Maths Olympics"
        context = {'title':title,'form':form}
        return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        pic.save()


        user = self.request.user
        email = user.email
        username = user.username
        events = ["Math Olympics"]
        context = {'username': username,'email': email,'events':events}
        # mydict = {'username': username}
        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        # return redirect("members:mail")
        return super().form_valid(form)


@method_decorator(csrf_exempt,name='dispatch')
class MathEventDetailView(LoginRequiredMixin,DetailView):
    model = MathEvent
    template_name = "members/mathEvent_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class MathEventIndCreateView(LoginRequiredMixin,CreateView):
    login_required = True
    form_class = MathEventIndividualForm
    template_name = 'members/profile_create.html'

    def get_context_data(self,*args, **kwargs):
        form = MathEventIndividualForm()
        form.instance.owner = self.request.user
        title = "Maths Olympics"
        context = {'title':title,'form':form}
        return context

    def get_success_url(self):
        return reverse('members:all')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pic = form.save(commit=False)
        # pic.save()

        user = self.request.user
        email = user.email
        username = user.username

        title = "Math Olympics"
        events = [title]
        context = {'username': username,'email': email,'events':events,'title':title}


        user.save()
        html_template = 'mail.html'
        html_message = render_to_string(html_template, context=context)
        subject = 'Welcome to RIC 2024'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()

        return super().form_valid(form)



@method_decorator(csrf_exempt,name='dispatch')
class MathEventIndDetailView(LoginRequiredMixin,DetailView):
    model = MathEventIndividual
    template_name = "members/mathEventInd_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class IDUpdateView(LoginRequiredMixin, View):
    template_name = 'members/update.html'
    success_url = reverse_lazy('members:all')
    def get(self, request, pk) :
        pic = get_object_or_404(IntegrationBee, id=pk, owner=self.request.user)
        form = IDForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(IntegrationBee, id=pk, owner=self.request.user)
        form = IDForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        # pic.abstractFormat =True
        pic.remarks = "Correct"
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)



class StudDetailUpdateView(LoginRequiredMixin, View):
    template_name = 'members/update.html'
    success_url = reverse_lazy('members:all')
    def get(self, request, pk) :
        pic = get_object_or_404(MathEvent, id=pk, owner=self.request.user)
        form = StudDetailForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(MathEvent, id=pk, owner=self.request.user)
        form = StudDetailForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        # pic.abstractFormat =True
        pic.remarks = "Correct"
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)



def mail(request):
    user = request.user
    email = user.email
    username = user.username
    # events = Event1.objects.all()
    bios = Bio.objects.filter(owner=user)
    events = bios.filter(owner=user).all()
    # events = events.event1.all()
    context = {'username': username,'email': email,'events':events}
    # context["workshop_bio"] = WorkshopBio.objects.all()
        # return context
    # context =
    return render(request, 'mail.html', context=context)

def success(request):
    return render(request, 'success.html', {})


# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.views.decorators.http import require_http_methods
# from datetime import datetime, timedelta
