from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = CKEditor5Field()
    answer = CKEditor5Field()
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.question

    def __unicode__(self):
        return self.question
