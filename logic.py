import os
import uuid

from django.shortcuts import get_object_or_404
from django.conf import settings

from core import files, models as core_models
from journal import models


def generate_jats_metadata(article, temp_file):
    pass


def prepare_temp_folder(issue=None, article=None):
    """
    Perpares a temp folder to store files for zipping
    :param issue: Issue Object
    :param article: Article object
    :return: Folder path, string
    """
    folder_string = uuid.uuid4()

    if issue:
        folder_string = 'portico_issue_{0}'.format(issue.pk)
    elif article:
        folder_string = 'portico_article_{0}'.format(article.pk)

    folder = os.path.join(settings.BASE_DIR, 'files', 'temp', folder_string)
    files.mkdirs(folder)

    return folder


def prepare_article(article, temp_folder):
    """
    Prepares an article for portico export
    :param article: Article object
    :param temp_folder: Folder string
    :return: None
    """
    article_folder = os.path.join(temp_folder, str(article.pk))
    files.mkdirs(article_folder)
    galleys = article.galley_set.all()

    try:
        xml_galley = galleys.get(file__mime_type__contains='/xml')
        files.copy_file_to_folder(xml_galley.file.self_article_path(), xml_galley.file.uuid_filename, article_folder)
    except core_models.Galley.DoesNotExist:
        generate_jats_metadata(article, temp_folder)


def prepare_export_for_issue(request):
    """
    Prepares an export for an issue
    :param request: HttpRequest object
    :return: Streaming zip file
    """
    issue_id = request.POST.get('export-issue', None)
    issue = get_object_or_404(models.Issue, pk=issue_id, journal=request.journal)

    temp_folder = prepare_temp_folder(issue=issue)

    print('Processing {issue}'.format(issue=issue))

    for article in issue.articles.all():
        print('Adding article: {title}'.format(title=article.title))
        prepare_article(article, temp_folder)

