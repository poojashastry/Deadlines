from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tasks
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.template import RequestContext
from models import Project


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
                request.session['currentUser'] = username
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

def createProject(request):
    participants = User.objects.all()
    # template = loader.get_template('Deadlines/createProject.html')
    # context = RequestContext(request)
    return render_to_response('Deadlines/createProject.html', {'participants': participants}, context_instance=RequestContext(request))

def signup(request):
    template = loader.get_template('Deadlines/signup.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def register(request):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    emailValidity = False
    token = get_token(request)
    if request.POST:
        message = ""

        # Gather user credentials from registration form

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        emailID = request.POST.get('emailID')
        retype_password = request.POST.get('retype_password')
        allUsernames = User.objects.values_list('username', flat=True)
        # Call helper function to check validity of emailID
        try:
            validate_email(emailID)
            emailValidity = True
        except ValidationError:
            emailValidity = False


        # Check for errors in the registration form

        for name in allUsernames:
                if name == username:
                    message = "Username already exists. Please try another one"
                    return render_to_response('Deadlines/signup.html', {'message': message}, context_instance= RequestContext(request))

        if not emailValidity or password != retype_password:
            if not emailValidity:
                message = message + " ,Email ID is invalid"
            if password != retype_password:
                message = message+", Passwords do not match"
            return render_to_response('Deadlines/signup.html', {'message': message}, context_instance= RequestContext(request))

        message = "Login Success"
        new_user = User.objects.create_user(username, emailID, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        return render_to_response('Deadlines/index.html',{'state': message, 'username': username}, context_instance= RequestContext(request))

def addProject(request):

    currentUser = request.session.get('currentUser')
    projectCreator = User.objects.get(username=currentUser)
    if request.POST:
        projectName = request.POST.get('projectName')
        projectDescription = request.POST.get('projectDescription')
        people = request.POST.getlist('participants[]')
        addProj = Project.objects.create(name=projectName,projectDescription=projectDescription)
        addProj.save()
        addProj.people.add(projectCreator)
        addProj.save()
        for person in people:
            usr = User.objects.get(username=person)
            addProj.people.add(usr)
            addProj.save()
    currentProjects = Project.objects.filter(people__username=currentUser)
    #addProj.people.add()
    return render_to_response('Deadlines/displayProject.html',{'currentUser':currentUser,'currentProjects' : currentProjects}, context_instance=RequestContext(request))

def projectDetails(request, projectName):
    selectedProject = Project.objects.get(name=projectName)
    projectTasks = Tasks.objects.filter(projects__name=projectName)
    return render_to_response('Deadlines/projectDetails.html',{'selectedProject': selectedProject, 'projectTasks': projectTasks})


