from django.db import models

# Create your models here.
from mongoengine import *

class User(Document):
    name = StringField(required=True , max_length=30, unique=True)
    emailID = EmailField(required=True, unique = True, primary_key=True)
    password = StringField(required=True)
    tasksAssigned = ListField(EmbeddedDocumentField(Tasks))

class Tasks(EmbeddedDocument):
    projectName = StringField()
    description = StringField()
    deadline = DateTimeField()

