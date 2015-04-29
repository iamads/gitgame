__author__ = 'ads'
from django.conf.urls import patterns, url
from moonmoon import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^payload/', views.payload, name='payload'),
                       url(r'^callback/', views.callback, name='callback'),
                       url(r'^show/', views.show, name='show'))