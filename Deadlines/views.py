from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tasks
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.models import User


# Create your views here.
def login_view(request):
    state = "Please Log In"
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Login success"
                tasks_assigned = Tasks.objects.filter(assignedTo__username=username)
            else:
                state = "Account Disabled"
        else:
            state = "Login Failed"
            return render_to_response('Deadlines/login.html', {'state': state, 'username': username})
    return render_to_response('Deadlines/index.html', {'state': state, 'username': username, 'tasks_assigned': tasks_assigned})


def index(request):
    return HttpResponse("Hi there! you are at the index page of deadlines.")

def usernames(request,first_name):
    tasks_assigned = Tasks.objects.filter(assignedTo__first_name=first_name)
    template = loader.get_template('Deadlines/index.html')
    context = RequestContext(request, {
        'tasks_assigned': tasks_assigned,
    })
    return HttpResponse(template.render(context))

def login_page(request):
    template = loader.get_template('Deadlines/login.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/deadlines/user/login/")

