from django.db import models
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Sponsor(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    pic  = models.ImageField(upload_to='sponsor')
    text = RichTextField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class SponsorReg(models.Model):

    CATEGORY_CHOICES = (
        ('Title Sponsorship','Title Sponsorship'),
        ('Co Sponsorship','Co Sponsorship'),
        ('Platinum Sponsorship','Platinum Sponsorship'),
        ('Gold Sponsorship','Gold Sponsorship'),
        ('Silver Sponsorship','Silver Sponsorship'),
        ('Bronze Sponsorship','Bronze Sponsorship'),
        ('Other','Other'),
    )
    TYPE = (
        ('Monetary Sponsorship','Monetary Sponsorship'),
        ('In Kind Sponsorship','In Kind Sponsorship')
    )
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(default="")
    poc_name = models.CharField(max_length=255,default="")
    poc_email = models.EmailField(default="")
    poc_number = PhoneNumberField(null=True,blank=True)
    poc_designation = models.CharField(max_length=100,null=True,blank=True)
    type_sponsor = models.CharField(choices=TYPE,max_length=100,null=True,blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100,null=True,blank=True)
    logo = models.ImageField(upload_to='sponsor')

    def __str__(self):
        return f"{self.name} from {self.company_name}"


class Cat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RICSponsor(models.Model):
    name = models.CharField(max_length=150)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE,null=True,blank=True)
    order = models.IntegerField(default=1,null=True,blank=True)
    pic = models.ImageField(upload_to='ricsponsor', height_field=None, width_field=None, max_length=None,default="")

    def __str__(self):
        return self.name