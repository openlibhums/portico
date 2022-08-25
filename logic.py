import os

from django.shortcuts import get_object_or_404

from core import files
from journal import models
from submission import models as submission_models
from utils.deposit import helpers as deposit_helpers


def prepare_article(request, article, temp_folder, article_only=False):
    """
    Prepares an article for portico export
    :param request: HttpRequest
    :param article: Article object
    :param temp_folder: Folder string
    :param article_only Boolean
    :return: None
    """
    if article_only:
        article_folder = temp_folder
    else:
        article_folder = os.path.join(temp_folder, str(article.pk))

    files.mkdirs(article_folder)
    galleys = article.galley_set.all()

    xml_galley = deposit_helpers.get_best_deposit_xml_galley(article, galleys)
    if xml_galley:
        files.copy_file_to_folder(
            xml_galley.file.self_article_path(),
            xml_galley.file.uuid_filename,
            article_folder,
        )
        for image in xml_galley.images.all():
            files.copy_file_to_folder(
                image.self_article_path(),
                image.original_filename,
                article_folder,
            )
    else:
        deposit_helpers.generate_jats_metadata(article, article_folder)

    pdf_galley = deposit_helpers.get_best_deposit_pdf_galley(galleys)
    if pdf_galley:
        files.copy_file_to_folder(
            deposit_helpers.file_path(article.pk, pdf_galley.file.uuid_filename),
            pdf_galley.file.uuid_filename, article_folder,
        )

    html_galley = deposit_helpers.get_best_deposit_html_galley(galleys)
    if html_galley:
        files.copy_file_to_folder(
            deposit_helpers.file_path(article.pk, html_galley.file.uuid_filename),
            html_galley.file.uuid_filename,
            article_folder,
        )
        for image in html_galley.images.all():
            files.copy_file_to_folder(
                image.self_article_path(),
                image.original_filename,
                article_folder,
            )


def prepare_export_for_issue(request, file=False):
    """
    Prepares an export for an issue
    :param request: HttpRequest object
    :param file: Boolean, returns a file path rather than a HttpRequest
    :return: Streaming zip file
    """
    issue_id = request.POST.get('export-issue', None)
    issue = get_object_or_404(models.Issue, pk=issue_id, journal=request.journal)

    temp_folder, folder_string = deposit_helpers.prepare_temp_folder(request, issue=issue)

    print('Processing {issue}'.format(issue=issue))

    for article in issue.articles.all():
        prepare_article(request, article, temp_folder)

    deposit_helpers.zip_temp_folder(temp_folder)

    if file:
        return [
            '{folder}.zip'.format(folder=temp_folder),
            '{filename}.zip'.format(filename=folder_string)
        ]

    return files.serve_temp_file('{folder}.zip'.format(folder=temp_folder),
                                 '{filename}.zip'.format(filename=folder_string))


def prepare_export_for_article(request):
    """
    Prepares a single article for portico export
    :param request: HttpRequest
    :return: Streaming zip file
    """
    article_id = request.POST.get('export-article')
    article = get_object_or_404(submission_models.Article, pk=article_id, journal=request.journal)

    issue = article.primary_issue if article.primary_issue else article.issue
    temp_folder, folder_string = deposit_helpers.prepare_temp_folder(request, issue=issue, article=article)
    prepare_article(request, article, temp_folder, article_only=True)
    deposit_helpers.zip_temp_folder(temp_folder)

    return files.serve_temp_file('{folder}.zip'.format(folder=temp_folder),
                                 '{filename}.zip'.format(filename=folder_string))


def get_articles(request):
    """
    Returns a QuerySet of articles suitable for export
    :param request: HttpRequest
    :return: QuerySet of articles
    """
    return submission_models.Article.objects.filter(date_published__isnull=False,
                                                    stage=submission_models.STAGE_PUBLISHED,
                                                    journal=request.journal)
