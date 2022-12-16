from django.db import models
from django.utils import timezone


class Delivered(models.Model):
    issue = models.ForeignKey(
        'journal.Issue',
        on_delete=models.CASCADE,
    )
    sent_at = models.DateTimeField(default=timezone.now)
