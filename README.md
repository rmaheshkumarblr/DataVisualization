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

##### Deleting the old content from the database - Note everything on the database will be deleted.

If you are in early development cycle and don't care about your current database data you can just remove it and than migrate. But first you need to clean migrations dir

rm  your_app/migrations/*

rm db.sqlite3
python manage.py makemigrations
python manage.py migrate


##### Creating the Schema on the database
python manage.py migrate --run-syncdb


As per the recent discussions, objectives as follows:

Login Mechanism required
	My files option for that particular user information

Header Information 

ypodID, date, time, bme_temp, bme_P ,temperature_SHT,humidity_SHT,co2,wind_speed,wind_dir,quad_aux_one,quad_main_one,quad_aux_two, quad_main_two,quad_aux_three, quad_main_three,quad_aux_four,quad_main_four,fig_210_heat, fig210_sens,fig_280_heat, fig280_sens,bl_moccon,adc2_channel2,e2vo3_heat, e2vo3_sens,GPS

Information that is required while uploading highlighted in bold

Pod ID:
Location:
Start Date and Time:
End Date and Time:
Pod Use Type (e.g., ambient monitoring, indoor, mobile, or experiment) - make these click button options
Pollutants of Interest: VOCs (this should give them both sensors), O3, CO2 - make these click button options
Short description of pod use (1-3 sentences) (textbox for them to type this in) 

Better to use HighCharts than to use D3


##### Connecting to the PostGresSQL
psql -U postgres
create database datavisdb;
CREATE ROLE datavis WITH LOGIN PASSWORD 'data';
GRANT ALL PRIVILEGES ON DATABASE dataVisualizationdb TO dataVis;
ALTER USER dataVis CREATEDB; 

postgres -D /usr/local/var/postgres

