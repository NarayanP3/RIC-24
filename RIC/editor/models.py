from django.db import models
from members.models import RICEvent
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    ricevent = models.ForeignKey(RICEvent, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return str(self.ricevent) + ' : ' + str(self.editor)

    def __unicode__(self):
        return str(self.ricevent) + ' : ' + str(self.editor)