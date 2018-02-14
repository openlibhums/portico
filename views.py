from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from plugins.portico import plugin_settings, logic
from journal import models
from utils import setting_handler


def index(request):
    plugin = plugin_settings.get_self()
    issues = models.Issue.objects.filter(journal=request.journal)

    if request.POST and 'export-issue' in request.POST:
        logic.prepare_export_for_issue(request)

    template = 'portico/index.html'
    context = {
        'issues': issues,
    }

    return render(request, template, context)


def settings(request):
    plugin = plugin_settings.get_self()

    template = 'portico/index.html'
    context = {}

    return render(request, template, context)