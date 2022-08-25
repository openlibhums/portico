import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from janeway_ftp import sftp

from plugins.portico import logic
from utils.deposit import helpers as deposit_helpers
from journal import models


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

        request = deposit_helpers.create_fake_request(issue)
        zip_file, file_name = logic.prepare_export_for_issue(
            request,
            file=True
        )

        logging.info(
            'Zip file to send {file}'.format(
                file=zip_file,
            )
        )

        sftp.send_file_via_sftp(
            ftp_server=settings.PORTICO_FTP_SERVER,
            ftp_username=settings.PORTICO_FTP_USERNAME,
            ftp_password=settings.PORTICO_FTP_PASSWORD,
            ftp_server_key=settings.PORTICO_FTP_SERVER_KEY,
            remote_file_path='chips',
            file_path=zip_file,
            file_name=file_name,
        )

        os.unlink(zip_file)
