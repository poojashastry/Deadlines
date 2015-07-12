from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Tasks
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    return HttpResponse("Hi there! you are at the index page of deadlines.")

def usernames(request,name):
    tasks_assigned = Tasks.objects.filter(assignedTo__name=name)
    template = loader.get_template('Deadlines/index.html')
    context = RequestContext(request, {
        'tasks_assigned': tasks_assigned,
    })
    return HttpResponse(template.render(context))

