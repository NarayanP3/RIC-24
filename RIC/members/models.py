from django.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from ckeditor.fields import RichTextField
import uuid
from .validators import validate_file_extension

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


class Subdomain(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Workshop(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    name = RichTextField()
    fee = models.IntegerField()
    venue = RichTextField(blank=True, null=True)
    desc = RichTextField(blank=True, null=True)
    organised_at = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    conducted_by = RichTextField(blank=True, null=True)
    link = models.URLField(max_length=200,default="www.ric.iitg.ac.in/",null=True,blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.owner.first_name,instance.owner.last_name, instance.dept,instance.institute, ext)
    return os.path.join('abstract', filename)


class Bio(models.Model):
    institute = models.CharField(max_length=50)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=None)
    abstract = models.FileField(upload_to=content_file_name, max_length=100, validators=[validate_file_extension])
    abstractFormat = models.BooleanField(default=True,null=True,blank=True)
    event1 = models.ManyToManyField(Event1, blank=True,null=True)
    number = PhoneNumberField()
    role = models.CharField(max_length=100, default="Student")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default="Name")
    email = models.CharField(max_length=150, default="abc@xyz.com")
    text = RichTextField(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    selected = models.BooleanField(default=False,null=True,blank=True)
    selected_oral = models.BooleanField(default=False,blank=True, null=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    iitg_student = models.BooleanField(default=False,null=True,blank=True)
    remarks = models.CharField(max_length=50,default="None",blank=True,null=True)
    def __str__(self):
        return self.owner.email

    def __unicode__(self):
        return self.owner.email

    def setpaymentid(self,id):
        print('test')
        print(id)
        self.razorpay_payment_id = id
        self.save()



class RICEvent(models.Model):
    institute = models.CharField(max_length=50)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=None)
    abstract = models.FileField(upload_to=content_file_name, max_length=100, validators=[validate_file_extension])
    abstractFormat = models.BooleanField(default=True,null=True,blank=True)
    event = models.ForeignKey(Event1, on_delete=models.CASCADE, blank=True, null=True)
    number = PhoneNumberField()
    role = models.CharField(max_length=100, default="Student")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default="Name")
    email = models.CharField(max_length=150, default="abc@xyz.com")
    text = RichTextField(blank=True, null=True)
    total = models.IntegerField(default=0,blank=True,null=True)
    selected = models.BooleanField(default=False,null=True,blank=True)
    selected_oral = models.BooleanField(default=False,blank=True, null=True)
    razorpay_payment_id = models.CharField( max_length=100,null=True,blank=True)
    iitg_student = models.BooleanField(default=False,null=True,blank=True)
    remarks = models.CharField(max_length=50,default="None",blank=True,null=True)
    def __str__(self):
        return self.owner.email

    def __unicode__(self):
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
    # event = models.ManyToManyField(ICEvent, blank=True,null=True)
    number = PhoneNumberField(null=True)
    role = models.CharField(max_length=100, default="Student")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = RichTextField(blank=True, null=True)
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
    text = RichTextField(blank=True, null=True)
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
    text = RichTextField(blank=True, null=True)

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
    text = RichTextField(blank=True, null=True)

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
    text = RichTextField(blank=True, null=True)

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
    text = RichTextField(blank=True, null=True)

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
    # name = RichTextField()
    fee = models.IntegerField()
    desc = RichTextField(blank=True, null=True)
    organised_at = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    conducted_by = RichTextField(blank=True, null=True)
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
    text = RichTextField(blank=True, null=True)
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
