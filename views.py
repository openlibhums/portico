from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from plugins.portico import plugin_settings
from utils import setting_handler

def index(request):
    plugin = plugin_settings.get_self()

    template = 'portico/index.html'
    context = {}

    return render(request, template, context)