from django.db import models

# Create your models here.
class RICYEAR(models.Model):
    year = models.IntegerField()

    def __unicode__(self):
        return str(self.year)
    def __str__(self):
        return str(self.year)