from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone

from journal import models as jm
from plugins.portico import models


class Command(BaseCommand):
    """
    Sends an issue archive to Portico
    """

    help = "Sends an all unsent issues to Portico for archiving"

    def handle(self, *args, **options):
        issues = jm.Issue.objects.filter(
            date__lte=timezone.now(),
        )

        for issue in issues:
            print('Processing {}'.format(issue))
            if not models.Delivered.objects.filter(issue=issue).exists():
                call_command('send_to_portico', issue.pk)
                models.Delivered.objects.create(
                    issue=issue,
                )
            else:
                print('Issue has previously been delievered to Portico')

