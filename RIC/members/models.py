from django.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

from django_ckeditor_5.fields import CKEditor5Field

import uuid
from .validators import validate_file_extension

from ric_year.models import RICYEAR
from django.core.validators import FileExtensionValidator

# Create your models here.
class Event1(models.Model):
    name = models.CharField(max_length=400)
    fee = models.IntegerField(default=50000,null=True)
    deadline = models.DateTimeField( null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Event2(models.Model):
    name = models.CharField(max_length=50)
    fee = models.IntegerField(default=50000,null=True)
    deadline = models.DateTimeField( null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class ICEvent(models.Model):
    name = models.CharField(max_length=50)
    fee = models.IntegerField(default=50000,null=True)
    deadline = models.DateTimeField( null=True, blank=True)


    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Dept(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Workshop(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    name = CKEditor5Field()
    fee = models.IntegerField()
    venue = CKEditor5Field(blank=True, null=True)
    desc = CKEditor5Field(blank=True, null=True)
    organised_at = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    conducted_by = CKEditor5Field(blank=True, null=True)
    link = models.URLField(max_length=200,default="www.ric.iitg.ac.in/",null=True,blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.owner.first_name,instance.owner.last_name, instance.dept,instance.institute, ext)
    return os.path.join('abstract', filename)

class Theme(models.Model):
    theme = models.CharField(max_length=250)

    def __unicode__(self):
        return self.theme
    def __str__(self):
        return self.theme

import json

class RICEvent(models.Model):
    institute = models.CharField(max_length=50)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=None)

    # participant_id = models.IntegerField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.participant_id:
    #         if self.owner:  # Assuming owner is the associated user
    #             self.participant_id = self.owner.id
    #     super().save(*args, **kwargs)


    default_abstract = '''<div>
                        <p style="font-size:14pt;line-height:normal;margin:0.55pt 120.4pt 0.55pt 96.4pt;orphans:0;text-align:center;widows:0;">
                            <a id="_Hlk133139167"><span style="font-family:'Times New Roman';"><strong>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit</strong></span></a>
                        </p>
                        <p style="font-size:10pt;line-height:normal;margin-bottom:0.35pt;margin-left:179.85pt;margin-right:204.35pt;orphans:0;text-align:center;widows:0;">
                            <span style="font-family:'Times New Roman';">Lorem Ipsum</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">1</span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:-0.6pt;">&nbsp;</span><span style="font-family:'Times New Roman';letter-spacing:-0.7pt;">Doerm</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">2</span><span style="font-family:'Times New Roman';letter-spacing:-0.3pt;">, Sitssn</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">3</span><span style="font-family:'Times New Roman';letter-spacing:-0.3pt;">&nbsp;and Muhttgbd</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">4</span>
                        </p>
                        <p style="font-size:10pt;line-height:normal;margin-bottom:0pt;margin-left:88.45pt;margin-right:112.45pt;orphans:0;text-align:center;widows:0;">
                            <span style="font-family:'Times New Roman';">Department of</span><span style="font-family:'Times New Roman';letter-spacing:-0.4pt;">&nbsp;</span><span style="font-family:'Times New Roman';">XYZ</span><span style="font-family:'Times New Roman';letter-spacing:-0.05pt;">&nbsp;</span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:-0.65pt;">&nbsp;Institute of ABC </span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:0.05pt;">&nbsp;</span><span style="font-family:'Times New Roman';">India (Country)</span>
                        </p>
                        <p style="font-size:10pt;line-height:115%;margin-bottom:10.45pt;text-align:center;">
                            <span style="font-family:'Times New Roman';">E-mail:&nbsp;</span><i><span style="font-family:'Times New Roman';">loremipum@abc.de.fg, loremipum@abc.de.fg,</span></i>
                        </p>
                        <p style="line-height:11.8pt;margin-bottom:0pt;margin-left:7.1pt;margin-right:29.6pt;orphans:0;text-align:center;text-indent:28.9pt;widows:0;">
                            <span style="font-family:'Times New Roman';font-size:12pt;vertical-align:2pt;"><strong>Abstract</strong></span>
                        </p>
                        <p style="font-size:10pt;line-height:104%;margin-bottom:0pt;margin-left:5.5pt;margin-right:27.8pt;orphans:0;text-align:justify;text-indent:30.5pt;widows:0;">
                            <span style="font-family:'Times New Roman';">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</span><br>
                            <span style="font-family:'Times New Roman';">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</span>
                        </p>
                        <p style="font-size:10pt;line-height:104%;margin-bottom:0pt;margin-left:5.5pt;margin-right:27.8pt;orphans:0;text-align:justify;text-indent:30.5pt;widows:0;">
                            <span style="font-family:'Times New Roman';"><strong>Keywords:&nbsp;</strong>Neque porro, quisquam est, qui dolorem ipsum, quia dolor sit amet, consectetur, adipisci velit</span>
                        </p>
                    </div>'''

    abstract = CKEditor5Field(default=default_abstract, config_name='extends')

    # abstract_file = models.FileField(upload_to='abstract/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])

    abstractFormat = models.BooleanField(default=True,null=True,blank=True)
    event = models.ForeignKey(Event1, on_delete=models.SET_NULL, blank=True, null=True)
    number = PhoneNumberField()
    role = models.CharField(max_length=100, default="Student")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default="Name")
    title = models.CharField(max_length=150, default="Title")
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null = True, blank=True)
    email = models.CharField(max_length=150, default="abc@xyz.com")
    text = CKEditor5Field(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    status = models.CharField(max_length=50, default='Pending')
    selected = models.BooleanField(default=False,null=True,blank=True)
    selected_oral = models.BooleanField(default=False,blank=True, null=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    iitg_student = models.BooleanField(default=False,null=True,blank=True)
    remarks = models.CharField(max_length=50,default="None",blank=True,null=True)
    # try_new = models.CharField(max_length=100,null=True,blank=True)
    # presenters = models.CharField(null=True, blank=True, max_length=400)




    ricyear = models.ForeignKey(RICYEAR, null=True, blank=True, on_delete=models.SET_NULL)

    presenters = models.TextField(null=True, blank=True)  # Change CharField to TextField

    # Override the save method to ensure presenters are stored as JSON
    def save(self, *args, **kwargs):
        if self.presenters:
            try:
                json.loads(self.presenters)  # Check if presenters can be deserialized
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for presenters")

        super().save(*args, **kwargs)

    # Method to get presenters as a Python object
    def get_presenters(self):
        if self.presenters:
            return json.loads(self.presenters)
        return []

    # Method to set presenters from a Python object
    def set_presenters(self, presenters):
        self.presenters = json.dumps(presenters)

    # Property to access presenters as a Python object
    @property
    def presenters_list(self):
        return self.get_presenters()

    # Property to set presenters from a Python object
    @presenters_list.setter
    def presenters_list(self, presenters):
        self.set_presenters(presenters)

    def _str_(self):
        return self.owner.email

    def _unicode_(self):
        return self.owner.email


    def setpaymentid(self,id):
        print('test')
        print(id)
        self.razorpay_payment_id = id
        self.save()


def ic_content_file_name(instance, filename):
    ext = filename.split('.')[-1]

    filename = "%s_%s_%s_%s.%s" % (instance.owner.first_name,instance.owner.last_name, instance.institute,instance.number, ext)
    return os.path.join('ic', filename)

class IC(models.Model):
    institute = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=150, default="Name")
    email = models.CharField(max_length=150, default="abc@xyz.com")
    icSubmission = models.FileField(upload_to=ic_content_file_name, max_length=100,blank=True,null=True)
    icSubmissionFormat = models.BooleanField(default=False,null=True,blank=True)
    event = models.ForeignKey(ICEvent, on_delete=models.CASCADE, blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null = True, blank=True)
    title = models.CharField(max_length=150, default="Title")

    # event = models.ManyToManyField(ICEvent, blank=True,null=True)
    number = PhoneNumberField(null=True)
    role = models.CharField(max_length=100, default="Student")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = CKEditor5Field(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    selected = models.BooleanField(default=False,null=True,blank=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    iitg_student = models.BooleanField(default=False,null=True,blank=True)
    remarks = models.CharField(max_length=500,default="None",blank=True,null=True)

    def __str__(self):
        return self.owner.email

    def __unicode__(self):
        return self.owner.email

    def setpaymentid(self,id):
        print('test')
        print(id)
        self.razorpay_payment_id = id
        self.save()


class Accommodation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,default="")
    college = models.CharField(max_length=300,null=True)
    address_line_1 = models.CharField(max_length=100,null=True)
    address_line_2 = models.CharField(max_length=100,null=True)
    pincode = models.CharField(max_length=10,null=True)
    number = PhoneNumberField(null=True)
    role = models.CharField(max_length=100, default="Student")
    state = models.CharField(max_length=50,null=True)
    within_radius = models.BooleanField(default=False,null=True)
    entry_date = models.DateField(null=True)
    event_rc_list = models.ManyToManyField(Event1, blank=True,null=True)
    event_ic_list = models.ManyToManyField(ICEvent, blank=True,null=True)
    total = models.IntegerField(default=200,blank=True,null=True)
    total = models.IntegerField(default=200,blank=True,null=True)
    getting_accommodation = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    remarks = models.CharField(max_length=50,default="None",null=True,blank=True)
    # Other fields as necessary

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class WorkshopBio(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=None)
    workshop = models.ManyToManyField(Workshop, blank=True,null=True)
    number = PhoneNumberField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    text = CKEditor5Field(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)

    def __str__(self):
        return self.owner.email

    def __unicode__(self):
        return self.owner.email

    def setpaymentid(self,id):
        print('test')
        print(id)
        self.razorpay_payment_id = id
        self.save()


class IntegrationBee(models.Model):

    CLASS_CHOICES = (

        ('B1','B1'),
        ('B2','B2'),
        ('B3','B3'),
        ('B4','B4'),
    )
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=50, unique=True, editable=False)
    school_college_name = models.CharField(max_length=100)
    school_college_address = models.CharField(max_length=200)
    id_card = models.FileField(upload_to='id_cards/intBee')
    class_name = models.CharField(choices=CLASS_CHOICES, max_length=10)
    number = PhoneNumberField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = CKEditor5Field(blank=True, null=True)

    selected = models.BooleanField(default=True,null=True,blank=True)

    remarks = models.CharField(max_length=50,default="None",null=True)
    # Add other fields as necessary

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = 'RIC2023-intBee-' + str(uuid.uuid4().int)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DifferentiaChallenge(models.Model):
    LEVEL_CHOICES = (
        ('XI','XI'),
        ('XII','XII'),
    )

    CLASS_CHOICES = (
        ('XI','XI'),
        ('XII','XII'),

    )
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    school_college_name = models.CharField(max_length=100)
    school_college_address = models.CharField(max_length=200)
    id_card = models.FileField(upload_to='id_cards/Dsino')

    class_name = models.CharField(choices=CLASS_CHOICES, max_length=10)
    # class_name = models.CharField(max_length=10)
    number = PhoneNumberField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = CKEditor5Field(blank=True, null=True)

    selected = models.BooleanField(default=True,null=True,blank=True)

    remarks = models.CharField(max_length=50,default="None",null=True,blank=True)
    # Add other fields as necessary

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = 'RIC2023-dsino-' + str(uuid.uuid4().int)
        super().save(*args, **kwargs)

class MathEvent(models.Model):
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    school_name = models.CharField(max_length=100)
    student_list = models.FileField(upload_to='mathOlym/student_lists')
    school_address = models.CharField(max_length=200)
    school_contact = PhoneNumberField()
    teacher_list = models.TextField()
    point_of_contact = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = CKEditor5Field(blank=True, null=True)

    selected = models.BooleanField(default=True,null=True,blank=True)

    remarks = models.CharField(max_length=50,default="None",null=True,blank=True)

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = 'RIC2023-mathOly-' + str(uuid.uuid4().int)
        super().save(*args, **kwargs)

class MathEventIndividual(models.Model):
    CLASS_CHOICES = (
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
        ('IX','IX'),
        ('X','X'),

    )

    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=20, unique=True, editable=False)
    number = PhoneNumberField(default="12345")
    school_name = models.CharField(max_length=100)
    id_card = models.FileField(upload_to='id_cards/mathOlym')
    class_name = models.CharField(choices=CLASS_CHOICES, max_length=10)
    school_address = models.CharField(max_length=200)
    school_contact = PhoneNumberField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = CKEditor5Field(blank=True, null=True)

    selected = models.BooleanField(default=True,null=True,blank=True)

    remarks = models.CharField(max_length=50,default="None",null=True,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = 'RIC2023-mathOly-' + str(uuid.uuid4().int)
        super().save(*args, **kwargs)


class ProblemState(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    # name = CKEditor5Field()
    fee = models.IntegerField()
    desc = CKEditor5Field(blank=True, null=True)
    organised_at = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    conducted_by = CKEditor5Field(blank=True, null=True)
    link = models.URLField(max_length=200,default="")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def hack_content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.owner.first_name,instance.owner.last_name, instance.problem_statement,instance.iitg_student, ext)
    return os.path.join('hackathon', filename)


class Hackathon(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem_statement = models.ForeignKey(ProblemState, on_delete=models.CASCADE,default=None,null=True)
    iitg_student = models.BooleanField(default=False,null=True,blank=True)
    text = CKEditor5Field(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    selected = models.BooleanField(default=False,null=True,blank=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    remarks = models.CharField(max_length=50,default="None",blank=True,null=True)
    submission = models.FileField(upload_to=hack_content_file_name, max_length=100)
    submissionFormat = models.BooleanField(default=True,null=True,blank=True)
    number = PhoneNumberField()

    # problem_state_priority = models.ManyToManyField(Event1, blank=True,null=True)
    # institute = models.CharField(max_length=50)
    # selected_oral = models.BooleanField(default=False,blank=True, null=True)

    def __str__(self):
        return self.owner.email

    def __unicode__(self):
        return self.owner.email

    def setpaymentid(self,id):
        print('test')
        print(id)
        self.razorpay_payment_id = id
        self.save()

