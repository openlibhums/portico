from django.conf.urls import url

from plugins.portico import views

urlpatterns = [
    url(r'^$', views.index, name='portico_index'),
]