from django.shortcuts import render,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# from .forms import UploadFileForm
from django.http import HttpResponse,JsonResponse
from models import Document
from forms import DocumentForm

import os
import pandas as pd
import json
import datetime as datetime
# Based on https://github.com/axelpale/minimal-django-file-upload-example


    # podId = models.CharField(max_length=30)
    # location = models.CharField(max_length=30)
    # startDate = models.DateField()
    # endDate = models.DateField()
    # podUseType = MultiSelectField(choices=USETYPE,max_choices=4,max_length=4)
    # pollutantOfInterest = MultiSelectField(choices=POLLUTANTOFINTEREST,max_choices=4,max_length=4)
    # podUseReason = models.TextField()
    # docfile = models.FileField(upload_to='documents/')


def index(request):
    # # Handle file upload
    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         newdoc = Document(podId=request.POST['podId'],
    #                           location=request.POST['location'],
    #                           startDate=request.POST['startDate'],
    #                           endDate=request.POST['endDate'],
    #                           podUseType=request.POST['podUseType'],
    #                           pollutantOfInterest=request.POST['pollutantOfInterest'],
    #                           podUseReason=request.POST['podUseReason'],
    #                           docfile=request.FILES['docfile']
    #                          )
    #         newdoc.save()

    #         # Redirect to the document list after POST
    #         return HttpResponseRedirect(reverse('index'))
    # else:
    #     form = DocumentForm()  # A empty, unbound form

    # # Load documents for the list page
    # documents = Document.objects.all()

    # # Render list page with the documents and the form
    return render(
        request,
        'index.html'
        )


def documents(request):
    # readCSV = pd.read_csv(locationOfDocument)
    locationOfDocument=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media' + request.path
    # return redirect('/display/'+locationOfDocument)
    # url = reverse('display', kwargs={'locationOfDocument': locationOfDocument})
    # return HttpResponseRedirect(url)
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


def uploadedFiles(request):
    # Load documents for the list page
    documents = Document.objects.all()

    return render(
        request,
        'displayUploadedFiles.html',
        {'documents': documents}
        )

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
                              docfile=request.FILES['docfile']
                             )
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
        print "One"
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



    # return render(
    #     request,
    #     'display.html',
    #     {'displayContent': json.dumps(outputContent)}
    #     )

    # return JsonResponse(json.dumps(outputContent),safe=False)

    # response = HttpResponse()
    # response.write("Hello, Mahesh. Welcome to Data Visualization.")
    # response.write(json.dumps(outputContent))#, content_type="text/json")
    # return HttpResponse(response)
    # return HttpResponse("Hello, Mahesh. Welcome to Data Visualization.")

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

def multipleDataAnalysis(request, locationOfDocument1, locationOfDocument2):
    print locationOfDocument1 + " " + locationOfDocument2