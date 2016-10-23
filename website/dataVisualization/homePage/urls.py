from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^documents/', views.documents, name='documents'),
    url(r'^display/(?P<locationOfDocument>.*)$', views.display, name='display'),
    url(r'^uploadedFiles/', views.uploadedFiles, name='uploadedFiles'),
    url(r'^uploadAFile/', views.uploadAFile, name='uploadAFile'),
    url(r'^dataAnalysis/(?P<locationOfDocument>.*)$', views.dataAnalysis, name='dataAnalysis'),
    # (?P<path>.*)$
]
