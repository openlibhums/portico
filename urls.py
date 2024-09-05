from django.urls import re_path

from plugins.portico import views

urlpatterns = [
    re_path(r'^$', views.index, name='portico_index'),
]
