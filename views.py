from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from plugins.portico import plugin_settings, logic
from journal import models


def index(request):
    plugin = plugin_settings.get_self()
    issues = models.Issue.objects.filter(journal=request.journal)

    if request.POST and 'export-issue' in request.POST:
        return logic.prepare_export_for_issue(request)

    if request.POST and 'export-article' in request.POST:
        return logic.prepare_export_for_article(request)

    template = 'portico/index.html'
    context = {
        'issues': issues,
        'articles': logic.get_articles(request)
    }

    return render(request, template, context)


def settings(request):
    plugin = plugin_settings.get_self()

    template = 'portico/index.html'
    context = {}

    return render(request, template, context)