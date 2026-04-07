from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class RepairPartMixin(TimeStampedModel):
    class CategoryChoice(models.TextChoices):
        ENGINE_TRANSMISSION = 'Engine and Transmission', 'Engine and Transmission'
        BRAKES_WHEELS = 'Brakes and Wheels', 'Brakes and Wheels'
        SUSPENSION_STEERING = 'Suspension and Steering', 'Suspension and Steering'
        ELECTRICAL_SYSTEM = 'Electrical System', 'Electrical System'
        FUEL_SYSTEM = 'Fuel System', 'Fuel System'
        OTHER = 'Other', 'Other'

    category = models.CharField(
        max_length=50,
        choices=CategoryChoice.choices
    )

    description = models.TextField()

    class Meta:
        abstract = True


class SoftDeletionMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


    def delete(self,  *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

