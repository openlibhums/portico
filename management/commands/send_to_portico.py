from ftplib import FTP, error_perm
import logging
from mock import Mock
import os
import paramiko

from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpRequest

from plugins.portico import logic
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

        ssh = paramiko.SSHClient()
        ecdsa_key = getattr(settings, 'PORTICO_FTP_SERVER_KEY', '')
        if ecdsa_key:
            key = paramiko.ecdsakey.ECDSAKey(
                data=paramiko.py3compat.decodebytes(ecdsa_key.encode("utf8"))
            )
            ssh.get_host_keys().add(
                hostname=settings.PORTICO_FTP_SERVER,
                keytype="ecdsa",
                key=key,
            )
        else:
            logging.warning("No PORTICO_FTP_SERVER_KEY configured")
            ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())

        ssh.connect(
            settings.PORTICO_FTP_SERVER,
            username=settings.PORTICO_FTP_USERNAME,
            password=settings.PORTICO_FTP_PASSWORD,
        )
        sftp = ssh.open_sftp()
        remote_path = 'janeway/{}'.format(file_name)
        sftp.put(
            zip_file,
            remote_path,
        )

        # Close SFTP Session and unlink the zip file
        ssh.close()
        os.unlink(zip_file)

