from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^createuser/$', views.create_user_view),
    url('^auth/*', views.login_view),
    url('^home/$', views.home_view),
    url('^logout/$', views.logout_view),
    url(r'^documents/', views.documents, name='documents'),
    url(r'^display/(?P<locationOfDocument>.*)$', views.display, name='display'),
    url(r'^uploadedFiles/', views.uploadedFiles, name='uploadedFiles'),
    url(r'^uploadedFilesFiltered/(?P<projectName>.*)/(?P<mentorName>.*)/(?P<school>.*)$', views.uploadedFilesFiltered, name='uploadedFilesFiltered'),
    url(r'^personalUploadedFiles/', views.personalUploadedFiles, name='personalUploadedFiles'),
    url(r'^uploadAFile/', views.uploadAFile, name='uploadAFile'),
    url(r'^dataAnalysis/(?P<locationOfDocument1>.*)/(?P<locationOfDocument2>.*)$', views.dataAnalysis, name='dataAnalysis'),
    url(r'^getRawCSV/(?P<locationOfDocument1>.*)/', views.getRawCSV, name='getRawCSV'),
    url(r'^getSelectedCSV/(?P<locationOfDocument1>.*)/', views.getSelectedCSV, name='getSelectedCSV'),
    # url(r'^dataAnalysis/(?P<locationOfDocument>.*)$', views.dataAnalysis, name='dataAnalysis'),
    # (?P<path>.*)$
]
