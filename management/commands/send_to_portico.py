from ftplib import FTP, error_perm
import logging
from mock import Mock
import os

from django.core.management.base import BaseCommand
from django.http import HttpRequest

from plugins.portico import plugin_settings, logic
from journal import models


def create_fake_request(issue):
    request = Mock(HttpRequest)
    request.GET = Mock()
    request.journal = issue.journal
    request.POST = {'export-issue': issue.pk}

    return request


class Command(BaseCommand):
    """
    Sends an issue archive to Portico
    """

    help = "Sends an issue to Portico for archiving"

    def add_arguments(self, parser):
        """Adds arguments to Django's management command-line parser.

        :param parser: the parser to which the required arguments will be added
        :return: None
        """
        parser.add_argument('issue_id', type=int)

    def handle(self, *args, **options):
        issue = models.Issue.objects.get(
            pk=options.get('issue_id')
        )

        logging.info(
            'Issue to be archived: {issue} from {journal}'.format(
                issue=issue,
                journal=issue.journal.name
            )
        )

        request = create_fake_request(issue)
        zip_file, file_name = logic.prepare_export_for_issue(
            request,
            file=True
        )

        logging.info(
            'Zip file to send {file}'.format(
                file=zip_file,
            )
        )

        file_to_send = open(zip_file, 'rb')

        ftp = FTP(plugin_settings.PORTICO_FTP_SERVER)
        ftp.login(
            user=plugin_settings.PORTICO_FTP_USERNAME,
            passwd=plugin_settings.PORTICO_FTP_PASSWORD
        )
        try:
            ftp.mkd('janeway')
        except error_perm:
            # janeway dir exists, skip
            pass

        ftp.cwd('janeway')

        ftp.storbinary(
            'STOR {file_name}'.format(file_name=file_name),
            file_to_send
        )

        # Close file, FTP Session and unlink the zip file
        file_to_send.close()
        ftp.quit()
        os.unlink(zip_file)

