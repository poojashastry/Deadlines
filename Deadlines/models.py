from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    emailID = models.EmailField(primary_key=True)
    password = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Tasks(models.Model):
    project = models.CharField(max_length=40)
    taskDescription = models.TextField()
    deadline = models.DateField()
    assignedTo = models.ForeignKey(User)

    def __unicode__(self):
        return self.project
