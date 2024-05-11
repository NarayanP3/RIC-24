from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from members.models import Dept

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    pic = models.ImageField(upload_to="event")
    subtitle = models.CharField(max_length=50)
    content = CKEditor5Field()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=50)
    subtitle = CKEditor5Field()
    pic = models.ImageField(upload_to='speakers', height_field=None, width_field=None, max_length=None)
    content = CKEditor5Field()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class DeptSpeaker(models.Model):
    name = models.CharField(max_length=150)
    subtitle = CKEditor5Field()
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to='dept_speakers', height_field=None, width_field=None, max_length=None)
    content = CKEditor5Field()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name