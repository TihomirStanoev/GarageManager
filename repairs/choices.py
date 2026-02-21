from django.db import models


class StatusChoice(models.TextChoices):
    DRAFT = 'Draft', 'Draft'
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'











