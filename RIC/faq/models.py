from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = RichTextField()
    answer = RichTextField()
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.question

    def __unicode__(self):
        return self.question
