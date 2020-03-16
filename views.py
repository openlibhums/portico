from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib import messages

from plugins.portico import plugin_settings, logic
from journal import models
from security import decorators


@decorators.editor_user_required
def index(request):
    plugin = plugin_settings.get_self()

    if request.journal:
        issues = models.Issue.objects.filter(journal=request.journal)
    else:
        issues = models.Issue.objects.all().order_by('journal__code')

    if request.POST:

        if 'export-issue' in request.POST:
            return logic.prepare_export_for_issue(request)

        if 'export-article' in request.POST:
            return logic.prepare_export_for_article(request)

        if 'send-to-portico' in request.POST:
            export_id = request.POST.get('send-to-portico')
            call_command('send_to_portico', export_id)

        messages.add_message(
            request,
            messages.INFO,
            'Command complete.'
        )

        return redirect(reverse('portico_index'))

    template = 'portico/index.html'
    context = {
        'issues': issues,
        'articles': logic.get_articles(request)
    }

    return render(request, template, context)


@decorators.editor_user_required
def settings(request):
    plugin = plugin_settings.get_self()

    template = 'portico/index.html'
    context = {}

    return render(request, template, context)
