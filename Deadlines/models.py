from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

'''class User(models.Model):
    name = models.CharField(max_length=30)
    emailID = models.EmailField(primary_key=True)
    password = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name'''

class Project(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    projectDescription = models.TextField(max_length=100)
    people = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

class Tasks(models.Model):
    projects = models.ManyToManyField(Project)
    task_name = models.CharField(max_length=40,primary_key=True)
    task_description = models.TextField(max_length=100)
    deadline = models.DateField()
    assignedTo = models.ForeignKey(User)

    def __unicode__(self):
        return self.task_name




