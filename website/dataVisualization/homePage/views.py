import os
import pandas as pd
import json
import datetime as datetime
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from models import Document
from forms import DocumentForm, LoginForm, CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from wsgiref.util import FileWrapper
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import csv


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
                    print
                    'Got Next parameter'
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
    locationOfDocument = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media' + request.path
    print
    locationOfDocument
    outputContent = []
    with open(locationOfDocument) as fileHandler:
        for line in fileHandler:
            dictContent = {}
            line = line.strip()
            if (len(line) > 0):
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
    print
    locationOfDocument
    outputContent = []
    with open(locationOfDocument) as fileHandler:
        for line in fileHandler:
            dictContent = {}
            line = line.strip()
            if (len(line) > 0):
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
    #Dhruv @07/10/21 - Added filter to show only files from October 2019
    documents = Document.objects.all()[1416:]

    # filterDict = {}
    # if projectName != "":
    #     filterDict['projectName'] = projectName
    # if mentorName != "":
    #     filterDict['mentorName'] = mentorName
    # if school != "":
    #     filterDict['school'] = school

    # documents = documents.filter(**filterDict)

    return render(
        request,
        'displayUploadedFiles.html',
        {'documents': documents}
    )


@login_required
def uploadedFilesFiltered(request, projectName, mentorName, school):
    # Load documents for the list page
    documents = Document.objects.all()
    print
    projectName, mentorName, school

    # filterDict = {}
    # if projectName != "":
    #     filterDict['projectName'] = projectName
    # if mentorName != "":
    #     filterDict['mentorName'] = mentorName
    # if school != "":
    #     filterDict['school'] = school

    # documents = documents.filter(**filterDict)
    documents = documents.filter(projectName__icontains=projectName).filter(mentorName__icontains=mentorName).filter(
        school__icontains=school)

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


def includeConcentationToDataFrame(df):
    VOC1_ppm_min = df.fig210_sens.min(axis=0)
    VOC2_ppm_min = df.fig280_sens.min(axis=0)

    CO2_ppm_min = df.CO2.min(axis=0)
    CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
    CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)

    # CO_ppm_min = df.CO.min(axis=0)
    CO_ppm_slope = 0.0008  # ((5000-390)/float(4500 - CO_ppm_min))
    CO_ppm_int = -1.965  # 5000 - (4500*CO_ppm_slope)

    O3_ppb_mean = df.e2vo3_sens.mean()
    O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
    O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
    O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))

    df['CO2_ppm'] = (CO2_ppm_slope * df['CO2']) + CO2_ppm_int
    df['CO_ppm'] = (CO_ppm_slope * df['CO']) + CO_ppm_int
    df['voc1_ppm'] = (20 * (df['fig210_sens'] - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)) + 1.8
    df['voc2_ppm'] = 10 * (df['fig280_sens'] - VOC2_ppm_min) / float(4500 - VOC2_ppm_min)
    df['O3_ppb'] = O3_ppb_slope * (1 / df['e2vo3_sens']) + O3_ppb_int
    
    
    if "PM1.0" in df:
        PM1_slope=1
        PM1_int=0
        df['PM1.0_ppm'] = (PM1_slope * df['PM1.0']) + PM1_int

    if "PM2.5" in df:
        PM25_slope=1
        PM25_int=0
        df['PM2.5_ppm'] = (PM25_slope * df['PM2.5']) + PM25_int

    if "PM10" in df:
        PM10_slope=1
        PM10_int=0
        df['PM10_ppm'] = (PM10_slope * df['PM10']) + PM10_int
	
    return df


def averaging_from_old_file(path, fileName):
    df = pd.read_csv("media/" + path, header=0, usecols=[1, 2, 5, 6, 7, 22, 19, 21, 25],
                     names=["oldDate", "Time", "Temperature", "Humidity", "CO2", "CO", "fig210_sens", "fig280_sens",
                            "e2vo3_sens"], delimiter=",")[0,1,2,3,4,7,5,6,8]

    df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])

    times = pd.DatetimeIndex(df.Date)

    # # Minute Averaging
    groupedMinute = df.groupby([times.date, times.hour, times.minute])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO"].mean().reset_index()
    groupedMinute['Date'] = pd.to_datetime(groupedMinute['level_0']) + (
            pd.to_timedelta(groupedMinute['level_1'], unit='h') + pd.to_timedelta(groupedMinute['level_2'],
                                                                                  unit='m'))

    groupedMinute.drop(['level_0', 'level_1', 'level_2'], axis=1, inplace=True)
    groupedMinute = groupedMinute[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO']]
    groupedMinute = includeConcentationToDataFrame(groupedMinute)

    # # Hour Averaging
    groupedHour = df.groupby([times.date, times.hour])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO"].mean().reset_index()
    groupedHour['Date'] = pd.to_datetime(groupedHour['level_0']) + (pd.to_timedelta(groupedHour['level_1'], unit='h'))
    groupedHour.drop(['level_0', 'level_1'], axis=1, inplace=True)
    groupedHour = groupedHour[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO']]
    groupedHour = includeConcentationToDataFrame(groupedHour)

    # # Day Averaging
    groupedDaily = df.groupby([times.date])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO"].mean().reset_index()
    groupedDaily['Date'] = pd.to_datetime(groupedDaily['index']) + (pd.to_timedelta(1, unit='s'))
    groupedDaily.drop(['index'], axis=1, inplace=True)
    groupedDaily = groupedDaily[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO']]
    groupedDaily = includeConcentationToDataFrame(groupedDaily)

    fileName = fileName.split(".")[0]

    groupedMinute.to_csv(fileName + "_" + path.split(".")[0] + '_minute' + ".csv", index=False)
    groupedHour.to_csv(fileName + "_" + path.split(".")[0] + '_hour' + ".csv", index=False)
    groupedDaily.to_csv(fileName + "_" + path.split(".")[0] + '_daily' + ".csv", index=False)

    os.remove("media/" + path)

    return fileName + "_" + path.split(".")[0]


def averaging_from_new_file(path, fileName):

    df = pd.read_csv("media/" + path, header=0, usecols=[1, 2, 5, 6, 7, 8, 9, 10, 25, 22, 24, 28],
                     names=["oldDate", "Time", "Temperature", "Humidity", "CO2", "PM1.0", "PM2.5", "PM10", "CO",
                            "fig210_sens", "fig280_sens",
                            "e2vo3_sens"], delimiter=",")[0,1,2,3,4,5,6,7,10,8,9,11]
    
    df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])

    times = pd.DatetimeIndex(df.Date)

    # # Minute Averaging
    groupedMinute = df.groupby([times.date, times.hour, times.minute])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO", "PM1.0", "PM2.5", "PM10"].mean().reset_index()
    groupedMinute['Date'] = pd.to_datetime(groupedMinute['level_0']) + (
            pd.to_timedelta(groupedMinute['level_1'], unit='h') + pd.to_timedelta(groupedMinute['level_2'],
                                                                                  unit='m'))

    groupedMinute.drop(['level_0', 'level_1', 'level_2'], axis=1, inplace=True)
    groupedMinute = groupedMinute[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO', "PM1.0", "PM2.5",
         "PM10"]]
    groupedMinute = includeConcentationToDataFrame(groupedMinute)

    # # Hour Averaging
    groupedHour = df.groupby([times.date, times.hour])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO", "PM1.0", "PM2.5", "PM10"].mean().reset_index()
    groupedHour['Date'] = pd.to_datetime(groupedHour['level_0']) + (pd.to_timedelta(groupedHour['level_1'], unit='h'))
    groupedHour.drop(['level_0', 'level_1'], axis=1, inplace=True)
    groupedHour = groupedHour[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO', "PM1.0", "PM2.5",
         "PM10"]]
    groupedHour = includeConcentationToDataFrame(groupedHour)

    # # Day Averaging
    groupedDaily = df.groupby([times.date])[
        'Temperature', 'Humidity', "CO2", "fig210_sens", "fig280_sens", "e2vo3_sens", "CO", "PM1.0", "PM2.5", "PM10"].mean().reset_index()
    groupedDaily['Date'] = pd.to_datetime(groupedDaily['index']) + (pd.to_timedelta(1, unit='s'))
    groupedDaily.drop(['index'], axis=1, inplace=True)
    groupedDaily = groupedDaily[
        ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO', "PM1.0", "PM2.5",
         "PM10"]]
    groupedDaily = includeConcentationToDataFrame(groupedDaily)

    fileName = fileName.split(".")[0]

    groupedMinute.to_csv(fileName + "_" + path.split(".")[0] + '_minute' + ".csv", index=False)
    groupedHour.to_csv(fileName + "_" + path.split(".")[0] + '_hour' + ".csv", index=False)
    groupedDaily.to_csv(fileName + "_" + path.split(".")[0] + '_daily' + ".csv", index=False)

    os.remove("media/" + path)

    return fileName + "_" + path.split(".")[0]


def averaging(path, fileName, fileType):
    if fileType == '1':
        return averaging_from_old_file(path, fileName)
    else:
        return averaging_from_new_file(path, fileName)


# def hourAveraging(path,fileName):
#     # # Hourly Averaging
#     df = pd.read_csv("media/"+path,header=0,usecols=[1,2,5,6,7,19,21,25],names=["oldDate", "Time", "Temperature","Humidity","CO2","fig210_sens","fig280_sens","e2vo3_sens"],delimiter=",")[0,1,2,3,4,7,5,6,8]
#     df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])
#     times = pd.DatetimeIndex(df.Date)

#     grouped = df.groupby([times.date, times.hour])['Temperature','Humidity',"CO2","fig210_sens","fig280_sens","e2vo3_sens"].mean().reset_index()
#     grouped['Date'] =  pd.to_datetime(grouped['level_0']) +  (pd.to_timedelta(grouped['level_1'],unit='h'))
#     grouped.drop(['level_0','level_1'],axis=1,inplace=True)
#     grouped = grouped[['Date','Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens']]


# # Daily Averaging

# df = pd.read_csv('test.txt',header=0,usecols=[1,2,5,6,7,19,21,25],names=["oldDate", "Time", "Temperature","Humidity","CO2","fig210_sens","fig280_sens","e2vo3_sens"],delimiter=",")[0,1,2,3,4,7,5,6,8]
# df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])
# times = pd.DatetimeIndex(df.Date)
# grouped = df.groupby([times.date])['Temperature','Humidity',"CO2","fig210_sens","fig280_sens","e2vo3_sens"].mean().reset_index()
# grouped['Date'] =  pd.to_datetime(grouped['index'])
# grouped.drop(['index'],axis=1,inplace=True)
# grouped = grouped[['Date','Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens']]


@login_required
def uploadAFile(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        some_file = File(request.FILES['docfile'])

        # import pdb
        # pdb.set_trace()
        # print averageMinuteFileContent
        if form.is_valid():
            path = default_storage.save('averaging.txt', ContentFile(some_file.read()))

            fileType = request.POST['typeOfFile']

            averageFileName = averaging(path, some_file.name, fileType)

            averageMinuteFile = averageFileName + '_minute.csv'
            averageHourFile = averageFileName + '_hour.csv'
            averageDailyFile = averageFileName + '_daily.csv'

            fileHandlerMinute = open(averageMinuteFile, 'rb')
            fileHandlerHour = open(averageHourFile, 'rb')
            fileHandlerDay = open(averageDailyFile, 'rb')

            averageMinuteFileHandle = File(fileHandlerMinute)
            averageHourFileHandle = File(fileHandlerHour)
            averageDayFileHandle = File(fileHandlerDay)

            # print averageMinuteFileHandle.__dict__
            # print some_file.__dict__
            newdoc = Document(podId=request.POST['podId'],
                              location=request.POST['location'],
                              startDate=request.POST['startDate'],
                              endDate=request.POST['endDate'],
                              podUseType=request.POST['podUseType'],
                              pollutantOfInterest=request.POST['pollutantOfInterest'],
                              podUseReason=request.POST['podUseReason'],
                              projectName=request.POST['projectName'],
                              mentorName=request.POST['mentorName'],
                              school=request.POST['school'],
                              userName=request.user.first_name,
                              typeOfFile=request.POST['typeOfFile'],
                              docfile=some_file,
                              averageMinuteFile=averageMinuteFileHandle,
                              averageHourFile=averageHourFileHandle,
                              averageDayFile=averageDayFileHandle
                              # averageMinuteFile=averageMinuteFileHandle
                              )

            # print request.FILES['docfile']
            newdoc.save()
            os.remove(averageMinuteFile)
            os.remove(averageHourFile)
            os.remove(averageDailyFile)

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
def getRawCSV(request, locationOfDocument1):
    filename = "media/" + locationOfDocument1
    if filename:
        output_file = FileWrapper(open(filename, 'rb'))
        response = HttpResponse(output_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % (locationOfDocument1)
        return response
    return HttpResponseNotFound('<h1>File not found</h1>')


@login_required
def getSelectedCSV(request, locationOfDocument1):
    filename = "media/" + locationOfDocument1
    if filename:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % (locationOfDocument1.split(".")[0] + ".csv")
        writer = csv.writer(response)
        df = pd.read_csv("media/" + locationOfDocument1,delimiter=',', header=None)
        noOfColumnsInDataframe=len(df.columns)
        if noOfColumnsInDataframe>26:
            writeFromNewFile(writer,locationOfDocument1,filename)
        else:
            writeFromOldFile(writer,locationOfDocument1,filename)
        return response  
    return HttpResponseNotFound('<h1>File not found</h1>')
def writeFromOldFile(writer,locationOfDocument1,filename):
    # Writing from old file
    writer.writerow(
            ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO', 'CO2_ppm',
             'CO_ppm', 'voc1_ppm', 'voc2_ppm', 'O3_ppb'])
    df = pd.read_csv("media/" + locationOfDocument1, header=0, usecols=[1, 2, 5, 6, 7, 22, 19, 21, 25],
                         names=["oldDate", "Time", "Temperature", "Humidity", "CO2", "CO", "fig210_sens", "fig280_sens",
                                "e2vo3_sens"], delimiter=",")[0,1,2,3,4,5,6,7,10,8,9,11]
    df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])
    VOC1_ppm_min = df.fig210_sens.min(axis=0)
    VOC2_ppm_min = df.fig280_sens.min(axis=0)
    CO2_ppm_min = df.CO2.min(axis=0)
    CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
    CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)
    CO_ppm_slope = 0.0008
    CO_ppm_int = -1.965
    O3_ppb_mean = df.e2vo3_sens.mean()
    O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
    O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
    O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))
    with open(filename) as fileHandler:
        for line in fileHandler:
            line = line.strip()
            if (len(line) > 0):
                splitLine = line.split(',')
                writer.writerow(
                        [splitLine[1] + " " + splitLine[2],
                         splitLine[5],
                         splitLine[6],
                         splitLine[7],
                         splitLine[19],
                         splitLine[21],
                         splitLine[25],
                         splitLine[22],
                         (CO2_ppm_slope * float(splitLine[7])) + CO2_ppm_int,
                         (CO_ppm_slope * float(splitLine[13])) + CO_ppm_int,
                         (20 * (float(splitLine[19]) - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)) + 1.8,
                         10 * (float(splitLine[21]) - VOC2_ppm_min) / float(4500 - VOC2_ppm_min),
                         O3_ppb_slope * (1 / float(splitLine[25])) + O3_ppb_int
                         ])
def writeFromNewFile(writer,locationOfDocument1,filename):
    # Writing from new file
    writer.writerow(
            ['Date', 'Temperature', 'Humidity', 'CO2', 'fig210_sens', 'fig280_sens', 'e2vo3_sens', 'CO', 'CO2_ppm',
             'CO_ppm', 'voc1_ppm', 'voc2_ppm', 'O3_ppb','PM1.0','PM1.0_ppm','PM2.5','PM2.5_ppm','PM10','PM10_ppm'])
    df = pd.read_csv("media/" + locationOfDocument1, header=0, usecols=[1, 2, 5, 6, 7, 8, 9, 10, 25, 22, 24, 28],
                     names=["oldDate", "Time", "Temperature", "Humidity", "CO2", "PM1.0", "PM2.5", "PM10", "CO",
                            "fig210_sens", "fig280_sens",
                            "e2vo3_sens"], delimiter=",")[0,1,2,3,4,5,6,7,10,8,9,11]

    df['Date'] = pd.to_datetime(df['oldDate'] + ' ' + df['Time'])
    VOC1_ppm_min = df.fig210_sens.min(axis=0)
    VOC2_ppm_min = df.fig280_sens.min(axis=0)
    CO2_ppm_min = df.CO2.min(axis=0)
    CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
    CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)
    CO_ppm_slope = 0.0008
    CO_ppm_int = -1.965
    O3_ppb_mean = df.e2vo3_sens.mean()
    O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
    O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
    O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))
    PM1_slope=1
    PM1_int=0
    PM25_slope=1
    PM25_int=0
    PM10_slope=1
    PM10_int=0
    

    with open(filename) as fileHandler:
        for line in fileHandler:
            line = line.strip()
            if (len(line) > 0):
                splitLine = line.split(',')
                writer.writerow(
                        [splitLine[1] + " " + splitLine[2],
                         splitLine[5],
                         splitLine[6],
                         splitLine[7],
                         splitLine[22],
                         splitLine[24],
                         splitLine[28],
                         splitLine[25],
                         (CO2_ppm_slope * float(splitLine[7])) + CO2_ppm_int,
                         (CO_ppm_slope * float(splitLine[25])) + CO_ppm_int,
                         (20 * (float(splitLine[22]) - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)) + 1.8,
                         10 * (float(splitLine[24]) - VOC2_ppm_min) / float(4500 - VOC2_ppm_min),
                         O3_ppb_slope * (1 / float(splitLine[28])) + O3_ppb_int,
                         splitLine[8],
                         (PM1_slope*float(splitLine[8]))+ PM1_int,
                         splitLine[9],
                        (PM25_slope*float(splitLine[9]))+ PM25_int,
                         splitLine[10],
                        (PM10_slope*float(splitLine[10]))+ PM10_int
                         ])

def getContentsOfTxtFile(locationOfDocument):
    outputContent = []

    CO2_ppm_min = float("inf")
    CO2_ppm_slope = 0
    CO2_ppm_int = 0

    # CO_ppm_min = float("inf")
    CO_ppm_slope = 0
    CO_ppm_int = 0

    O3_ppb_sum = 0
    O3_ppb_mean_inverse = 0
    O3_ppb_slope = 0
    O3_ppb_int = 0

    VOC1_ppm_min = pd.read_csv("media/" + locationOfDocument, header=0, usecols=[19], delimiter=",").min(axis=0).values[
        0]
    VOC2_ppm_min = pd.read_csv("media/" + locationOfDocument, header=0, usecols=[21], delimiter=",").min(axis=0).values[
        0]

    Count_To_Find_Mean = 0

    with open("media/" + locationOfDocument) as fileHandler:
        for line in fileHandler:
            dictContent = {}
            specialContent = {}
            line = line.strip()
            if (len(line) > 0):
                Count_To_Find_Mean += 1
                splitLine = line.split(',')
                # Calculated Value for Plots
                CO2_ppm_min = min(CO2_ppm_min, float(splitLine[7]))
                # CO_ppm_min = min(CO_ppm_min,float(splitLine[13]))
                O3_ppb_sum += float(splitLine[25])
                # Default Value for Plots
                dictContent['Date'] = splitLine[1] + " " + splitLine[2]
                dictContent['Temperature'] = splitLine[5]
                dictContent['Humidity'] = splitLine[6]
                dictContent['CO2'] = splitLine[7]
                dictContent['CO'] = splitLine[13]
                dictContent['fig210_sens'] = splitLine[19]
                dictContent['fig280_sens'] = splitLine[21]
                dictContent['e2vo3_sens'] = splitLine[25]
                dictContent['PM1.0'] = splitLine[8]
                dictContent['PM2.5'] = splitLine[9]
                dictContent['PM10'] = splitLine[10]
                dictContent['voc1_ppm'] = (float(splitLine[19]) - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)
                dictContent['voc2_ppm'] = (float(splitLine[21]) - VOC2_ppm_min) / float(4500 - VOC2_ppm_min)
                outputContent.append(dictContent)
            else:
                # Just to avoid divide by zero
                Count_To_Find_Mean = 1
        # CO2 Equations Calculations
        CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
        CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)
        # CO Equations Calculations
        CO_ppm_slope = 0.0000283  # ((5000-390)/float(4500 - CO_ppm_min))
        CO_ppm_int = 0.0792  # 5000 - (4500*CO_ppm_slope)
        # O3 Equations Calculations
        O3_ppb_mean = O3_ppb_sum / float(Count_To_Find_Mean)
        O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
        O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
        O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))
        # Append the calculated useful value to JSON
        specialContent['CO2_ppm_slope'] = CO2_ppm_slope
        specialContent['CO2_ppm_int'] = CO2_ppm_int
        specialContent['CO_ppm_slope'] = CO_ppm_slope
        specialContent['CO_ppm_int'] = CO_ppm_int
        specialContent['O3_ppb_slope'] = O3_ppb_slope
        specialContent['O3_ppb_int'] = O3_ppb_int
        outputContent.append(specialContent)
    return outputContent


def getValueOfIndexIfPresent(list, index):
    try:
        return list[index]
    except IndexError:
        return 0


def getContentsOfCSVFile(locationOfDocument):
    df = pd.read_csv("media/" + locationOfDocument,delimiter=',', header=None)
    noOfColumnsInDataframe=len(df.columns)
    outputContent = []

    if noOfColumnsInDataframe==19:
        outputContent=getContentsOfNewCSVFile(locationOfDocument)
    else:
        outputContent=getContentsOfOldCSVFile(locationOfDocument)

    return outputContent
    


def getContentsOfOldCSVFile(locationOfDocument):

    outputContent = []
    CO2_ppm_min = float("inf")
    CO2_ppm_slope = 0
    CO2_ppm_int = 0

    # CO_ppm_min = float("inf")
    CO_ppm_slope = 0
    CO_ppm_int = 0

    O3_ppb_sum = 0
    O3_ppb_mean_inverse = 0
    O3_ppb_slope = 0
    O3_ppb_int = 0

    VOC1_ppm_min = pd.read_csv("media/" + locationOfDocument, header=1, usecols=[4], delimiter=",").min(axis=0).values[
        0]
    VOC2_ppm_min = pd.read_csv("media/" + locationOfDocument, header=1, usecols=[5], delimiter=",").min(axis=0).values[
        0]

    Count_To_Find_Mean = 0

    with open("media/" + locationOfDocument) as fileHandler:
        count = 0
        for line in fileHandler:
            count += 1
            if count == 1:
                continue
            dictContent = {}
            specialContent = {}
            line = line.strip()
            if (len(line) > 0):
                Count_To_Find_Mean += 1
                splitLine = line.split(',')
                # Calculated Value for Plots
                CO2_ppm_min = min(CO2_ppm_min, float(splitLine[3]))
                O3_ppb_sum += float(splitLine[6])
                # If CO exists then calculate for CO
                # CO_ppm_min = min(CO_ppm_min,float(getValueOfIndexIfPresent(splitLine,7)))
                # Default Value for Plots
                dictContent['Date'] = splitLine[0]
                dictContent['Temperature'] = splitLine[1]
                dictContent['Humidity'] = splitLine[2]
                dictContent['CO2'] = splitLine[3]
                dictContent['CO'] = getValueOfIndexIfPresent(splitLine, 7)
                dictContent['fig210_sens'] = splitLine[4]
                dictContent['fig280_sens'] = splitLine[5]
                dictContent['e2vo3_sens'] = splitLine[6]
                dictContent['voc1_ppm'] = (float(splitLine[4]) - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)
                dictContent['voc2_ppm'] = (float(splitLine[5]) - VOC2_ppm_min) / float(4500 - VOC2_ppm_min)
                outputContent.append(dictContent)
            else:
                # Just to avoid divide by zero
                Count_To_Find_Mean = 1
        # CO2 Equations Calculations
        CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
        CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)
        # CO Equations Calculations
        CO_ppm_slope = 0.0008 # ((5000-390)/float(4500 - CO_ppm_min))
        CO_ppm_int = -1.965  # 5000 - (4500*CO_ppm_slope)
        # O3 Equations Calculations
        O3_ppb_mean = O3_ppb_sum / float(Count_To_Find_Mean)
        O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
        O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
        O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))
        # Append the calculated useful value to JSON
        specialContent['CO2_ppm_slope'] = CO2_ppm_slope
        specialContent['CO2_ppm_int'] = CO2_ppm_int
        specialContent['CO_ppm_slope'] = CO_ppm_slope
        specialContent['CO_ppm_int'] = CO_ppm_int
        specialContent['O3_ppb_slope'] = O3_ppb_slope
        specialContent['O3_ppb_int'] = O3_ppb_int
        outputContent.append(specialContent)
    return outputContent


def getContentsOfNewCSVFile(locationOfDocument):

    outputContent = []
    CO2_ppm_min = float("inf")
    CO2_ppm_slope = 0
    CO2_ppm_int = 0

    # CO_ppm_min = float("inf")
    CO_ppm_slope = 0
    CO_ppm_int = 0

    O3_ppb_sum = 0
    O3_ppb_mean_inverse = 0
    O3_ppb_slope = 0
    O3_ppb_int = 0
    PM1_slope=1
    PM1_int=0
    PM25_slope=1
    PM25_int=0
    PM10_slope=1
    PM10_int=0

    VOC1_ppm_min = pd.read_csv("media/" + locationOfDocument, header=1, usecols=[4], delimiter=",").min(axis=0).values[
        0]
    VOC2_ppm_min = pd.read_csv("media/" + locationOfDocument, header=1, usecols=[5], delimiter=",").min(axis=0).values[
        0]

    Count_To_Find_Mean = 0

    with open("media/" + locationOfDocument) as fileHandler:
        count = 0
        for line in fileHandler:
            count += 1
            if count == 1:
                continue
            dictContent = {}
            specialContent = {}
            line = line.strip()
            if (len(line) > 0):
                Count_To_Find_Mean += 1
                splitLine = line.split(',')
                # Calculated Value for Plots
                CO2_ppm_min = min(CO2_ppm_min, float(splitLine[3]))
                O3_ppb_sum += float(splitLine[6])
                # If CO exists then calculate for CO
                # CO_ppm_min = min(CO_ppm_min,float(getValueOfIndexIfPresent(splitLine,7)))
                # Default Value for Plots
                #Date	Temperature	Humidity	CO2	fig210_sens	fig280_sens	e2vo3_sens	CO	PM1.0	PM2.5	PM10	CO2_ppm	CO_ppm	voc1_ppm	voc2_ppm	O3_ppb	PM1.0_ppm	PM2.5_ppm	PM10_ppm
                dictContent['Date'] = splitLine[0]
                dictContent['Temperature'] = splitLine[1]
                dictContent['Humidity'] = splitLine[2]
                dictContent['CO2'] = splitLine[3]
                dictContent['CO'] = getValueOfIndexIfPresent(splitLine, 7)
                dictContent['fig210_sens'] = splitLine[4]
                dictContent['fig280_sens'] = splitLine[5]
                dictContent['e2vo3_sens'] = splitLine[6]
                dictContent['voc1_ppm'] = (float(splitLine[4]) - VOC1_ppm_min) / float(4500 - VOC1_ppm_min)
                dictContent['voc2_ppm'] = (float(splitLine[5]) - VOC2_ppm_min) / float(4500 - VOC2_ppm_min)
                dictContent['PM1.0']=splitLine[8]
                dictContent['PM2.5']=splitLine[9]
                dictContent['PM10']=splitLine[10]
                dictContent['PM1.0_ppm']=splitLine[16]
                dictContent['PM2.5_ppm']=splitLine[17]
                dictContent['PM10_ppm']=splitLine[18]
                outputContent.append(dictContent)
            else:
                # Just to avoid divide by zero
                Count_To_Find_Mean = 1
        # CO2 Equations Calculations
        CO2_ppm_slope = ((5000 - 390) / float(4500 - CO2_ppm_min))
        CO2_ppm_int = 5000 - (4500 * CO2_ppm_slope)
        # CO Equations Calculations
        CO_ppm_slope = 0.0008  # ((5000-390)/float(4500 - CO_ppm_min))
        CO_ppm_int = -1.965 # 5000 - (4500*CO_ppm_slope)
        # O3 Equations Calculations
        O3_ppb_mean = O3_ppb_sum / float(Count_To_Find_Mean)
        O3_ppb_mean_inverse = (1 / float(O3_ppb_mean))
        O3_ppb_slope = ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))))
        O3_ppb_int = (35 - ((35 - 0) / float(O3_ppb_mean_inverse - (1 / float(3150))) * O3_ppb_mean_inverse))
        # Append the calculated useful value to JSON
        specialContent['CO2_ppm_slope'] = CO2_ppm_slope
        specialContent['CO2_ppm_int'] = CO2_ppm_int
        specialContent['CO_ppm_slope'] = CO_ppm_slope
        specialContent['CO_ppm_int'] = CO_ppm_int
        specialContent['O3_ppb_slope'] = O3_ppb_slope
        specialContent['O3_ppb_int'] = O3_ppb_int
        specialContent['PM1.0_ppm_slope']=PM1_slope
        specialContent['PM2.5_ppm_slope']=PM25_slope
        specialContent['PM10_ppm_slope']=PM10_slope
        specialContent['PM1.0_ppm_int']=PM1_int
        specialContent['PM2.5_ppm_int']=PM25_int
        specialContent['PM10_ppm_int']=PM10_int
        outputContent.append(specialContent)
    return outputContent


@login_required
def dataAnalysis(request, locationOfDocument1, locationOfDocument2):
    # Both file names are provided - Must Ideally never happen
    if locationOfDocument2 == "":
        if locationOfDocument1 == "":
            return render(request, 'displayDataAnalysis.html')

        # Only one file name is provided - TXT or CSV
        outputContent1 = []
        if locationOfDocument1.split(".")[1] == "txt":
            outputContent1 = getContentsOfTxtFile(locationOfDocument1)
            return render(request, 'displayDataAnalysis.html', {'displayContent1': json.dumps(outputContent1)})
        else:
            outputContent1 = getContentsOfCSVFile(locationOfDocument1)
            return render(request, 'displayDataAnalysis.html', {'displayContent1': json.dumps(outputContent1)})

    # Two file names are provided - TXT or CSV
    else:
        outputContent1 = []
        outputContent2 = []

        # Processing for the 1st file
        if locationOfDocument1.split(".")[1] == "txt":
            outputContent1 = getContentsOfTxtFile(locationOfDocument1)
        else:
            outputContent1 = getContentsOfCSVFile(locationOfDocument1)

        # Processing for the 2nd file
        if locationOfDocument2.split(".")[1] == "txt":
            outputContent2 = getContentsOfTxtFile(locationOfDocument2)
        else:
            outputContent2 = getContentsOfCSVFile(locationOfDocument2)

        return render(request, 'displayDataAnalysis.html',
                      {'displayContent1': json.dumps(outputContent1), 'displayContent2': json.dumps(outputContent2)})


@login_required
def multipleDataAnalysis(request, locationOfDocument1, locationOfDocument2):
    print
    locationOfDocument1 + " " + locationOfDocument2

