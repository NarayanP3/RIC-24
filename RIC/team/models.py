from django.db import models
from django.db.models.fields.related import ForeignKey



# Create your models here.
class Position(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150,default="",blank=True, null=True)


    def __str__(self):
        return self.title

class Dept(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254,null=True,blank=True)
    order = models.IntegerField(default=1)
    number = models.IntegerField(blank=True, null=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='team', height_field=None, width_field=None, max_length=None,default="",null=True,blank=True)


    def __str__(self):
        return self.name
    
class FacultyAdvisor(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254,null=True,blank=True)
    dept = models.CharField(max_length=50)