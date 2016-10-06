# DataVisualization
Data Visualization for a given dataset for the Mechanical Department (University of Colorado Boulder)

#### Initial Setup to get up and running with django
```
# Creating virtual environment
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
# Installing django framework
pip install django
# Creating a folder for the website
mkdir website
cd website
# Creating a project for data visualization
django-admin startproject dataVisualization
# Creating an app for the project
python manage.py startapp basicTemplate


```

##### Check Django version
```
python -m django --version
```

##### Deleting from Database
```
python manage.py shell
from django.db import models
from homePage.models import Document
Document.objects.filter().delete()
```

##### Get the server up and running 
```
python manage.py runserver
```

