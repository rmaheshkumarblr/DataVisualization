import os
import pandas as pd
import json
import datetime as datetime
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,JsonResponse
from models import Document
from forms import DocumentForm, LoginForm, CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def create_user_view(request):
    if request.method == 'GET':
        form = CreateUserForm()
        return render(request, 'create_user.html', {'form': form})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email_address']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['password_repeat']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if password == confirm_password:
                # check if user exists
                user = User.objects.filter(username=email).first()
                if not user:
                    new_user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    new_user.save()
                    return HttpResponseRedirect('/')
                else:
                    error = {
                        'msg': 'Account already exists'
                    }
                    return render(request, 'create_user.html', {
                        'form': form,
                        'error': error
                    })
            else:
                error = {
                    'msg': 'Passwords are not the same'
                }
                return render(request, 'create_user.html', {
                    'form': form,
                    'error': error
                })



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # authenticate
            email = form.cleaned_data['email_address']
            password = form.cleaned_data['password']

            user = authenticate(
                username=email,
                password=password
            )

            if user is not None:
                # authenticated
                # log in the user
                login(request, user)

                next_url = request.POST.get('next', None)

                if next_url:
                    print 'Got Next parameter'
                    return HttpResponseRedirect(next_url)

                return render(request, 'index.html', {
                    'user': user
                })
            else:
                # not authenticated
                error = {
                    'msg': 'Could not validate credentials'
                }
                return render(request, 'login.html', {
                    'form': form,
                    'error': error
                })

    else:
        user = request.user
        if user and user.is_authenticated():
            return HttpResponseRedirect('/')
        form = LoginForm()
        return render(request, 'login.html', {
            'form': form
        })


@login_required
def home_view(request):
    return render(request, 'index.html', {
        'user': request.user
    })


@login_required
def logout_view(request):
    user = request.user
    if user and user.is_authenticated():
        # log the user out
        logout(request)
    # redirect to login
    return HttpResponseRedirect('/')


def index(request):
    return render(
        request,
        'index.html'
        )


@login_required
def documents(request):
    locationOfDocument=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media' + request.path
    print locationOfDocument
    outputContent = []
    with open(locationOfDocument) as fileHandler:
        for line in fileHandler:
            dictContent = {}
            line = line.strip()
            if(len(line) > 0):
                splitLine = line.split(',')
                dictContent['date'] = splitLine[1] + " " + splitLine[2]
                # datetime.datetime.strptime(splitLine[1] + " " + splitLine[2],'%Y-%m-%d %H:%M:%S')
                dictContent['temperature'] = splitLine[6]
                outputContent.append(dictContent)
    # print json.dumps(outputContent)

    return render(
        request,
        'display.html',
        {'displayContent': json.dumps(outputContent)}
        )


@login_required
def display(request, locationOfDocument):
    print locationOfDocument
    outputContent = []
    with open(locationOfDocument) as fileHandler:
        for line in fileHandler:
            dictContent = {}
            line = line.strip()
            if(len(line) > 0):
                splitLine = line.split(',')
                dictContent['Date'] = splitLine[1] + " " + splitLine[2]
                dictContent['Temperature'] = splitLine[15]
                outputContent.append(dictContent)
    # print json.dumps(outputContent)

    return render(
        request,
        'display.html',
        {'displayContent': json.dumps(outputContent)}
        )


@login_required
def uploadedFiles(request):
    # Load documents for the list page
    documents = Document.objects.all()

    return render(
        request,
        'displayUploadedFiles.html',
        {'documents': documents}
        )



@login_required
def personalUploadedFiles(request):
    # Load documents for the list page
    documents = Document.objects.filter(userName=request.user.first_name)

    return render(
        request,
        'personalDisplayUploadedFiles.html',
        {'documents': documents}
        )


@login_required
def uploadAFile(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(podId=request.POST['podId'],
                              location=request.POST['location'],
                              startDate=request.POST['startDate'],
                              endDate=request.POST['endDate'],
                              podUseType=request.POST['podUseType'],
                              pollutantOfInterest=request.POST['pollutantOfInterest'],
                              podUseReason=request.POST['podUseReason'],
                              userName = request.user.first_name,
                              docfile=request.FILES['docfile']
                             )
            # print request.FILES['docfile']
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('uploadedFiles'))
    else:
        form = DocumentForm()  # A empty, unbound form
    # Render list page with the documents and the form
    return render(
        request,
        'upload.html',
        {'form': form}
        )


@login_required
def dataAnalysis(request, locationOfDocument1, locationOfDocument2):
    
    if locationOfDocument2 == "":
        if locationOfDocument1 == "":
            return render(
            request,
            'displayDataAnalysis.html',
            )
        outputContent1 = []
        with open("media/"+locationOfDocument1) as fileHandler:
            for line in fileHandler:
                dictContent1 = {}
                line = line.strip()
                if(len(line) > 0):
                    splitLine = line.split(',')
                    dictContent1['Date'] = splitLine[1] + " " + splitLine[2]
                    dictContent1['Temperature'] = splitLine[5]
                    dictContent1['Humidity'] = splitLine[6]
                    dictContent1['CO2'] = splitLine[7]
                    dictContent1['fig210_sens'] = splitLine[19]
                    dictContent1['fig280_sens'] = splitLine[21]
                    dictContent1['e2vo3_sens'] = splitLine[25]
                    outputContent1.append(dictContent1)
        return render(
            request,
            'displayDataAnalysis.html',
            {'displayContent1': json.dumps(outputContent1)}
            )
    else:
        outputContent1 = []
        with open("media/"+locationOfDocument1) as fileHandler:
            for line in fileHandler:
                dictContent1 = {}
                line = line.strip()
                if(len(line) > 0):
                    splitLine = line.split(',')
                    dictContent1['Date'] = splitLine[1] + " " + splitLine[2]
                    dictContent1['Temperature'] = splitLine[5]
                    dictContent1['Humidity'] = splitLine[6]
                    dictContent1['CO2'] = splitLine[7]
                    dictContent1['fig210_sens'] = splitLine[19]
                    dictContent1['fig280_sens'] = splitLine[21]
                    dictContent1['e2vo3_sens'] = splitLine[25]
                    outputContent1.append(dictContent1)
        outputContent2 = []
        with open("media/"+locationOfDocument2) as fileHandler:
            for line in fileHandler:
                dictContent2 = {}
                line = line.strip()
                if(len(line) > 0):
                    splitLine = line.split(',')
                    dictContent2['Date'] = splitLine[1] + " " + splitLine[2]
                    dictContent2['Temperature'] = splitLine[5]
                    dictContent2['Humidity'] = splitLine[6]
                    dictContent2['CO2'] = splitLine[7]
                    dictContent2['fig210_sens'] = splitLine[19]
                    dictContent2['fig280_sens'] = splitLine[21]
                    dictContent2['e2vo3_sens'] = splitLine[25]
                    outputContent2.append(dictContent2)
        print "Two"
        return render(
            request,
            'displayDataAnalysis.html',
            {'displayContent1': json.dumps(outputContent1),'displayContent2': json.dumps(outputContent2)}
            )

@login_required
def multipleDataAnalysis(request, locationOfDocument1, locationOfDocument2):
    print locationOfDocument1 + " " + locationOfDocument2