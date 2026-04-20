from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from cars.choices import BrandChoice, EngineChoice
from cars.validators import ProductionYearValidator, PlateValidator
from common.managers import SoftDeleteManager
from common.models import TimeStampedModel, SoftDeletionMixin
from django.conf import settings
from cloudinary.models import CloudinaryField

class Car(SoftDeletionMixin, TimeStampedModel):
    brand = models.CharField(
        max_length=30,
        choices=BrandChoice.choices
    )

    model = models.CharField(
        max_length=40)

    plate = models.CharField(
        max_length=10,
        unique=True,
        validators = [PlateValidator()]
    )

    year = models.PositiveIntegerField(
        validators=[ProductionYearValidator()])

    engine_type = models.CharField(
        max_length=10,
        choices=EngineChoice.choices
    )

    mileage = models.PositiveIntegerField()

    image = CloudinaryField(
        'cars/images',
        null=True, blank=True
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='cars',
        null=True, blank=True
    )


    objects = SoftDeleteManager()
    all_objects = models.Manager()


    class Meta:
        ordering = ['brand', 'model']


    @property
    def brand_model(self):
        return f'{self.brand} {self.model}'



    def _validate_deletable(self):
        is_invoiced = self.repairs.filter(is_invoiced=True).exists()
        is_owned = self.owner

        if is_owned:
            raise ValidationError('Cannot delete car: cannot delete a car that has an owner assigned..')

        if is_invoiced:
            raise ValidationError('Cannot delete car: one or more repairs have already been invoiced.')


    def delete(self, *args, **kwargs):
        self._validate_deletable()
        repairs = self.repairs.all()

        repairs.update(is_deleted=True, deleted_at=timezone.now())

        super().delete(*args, **kwargs)


    def hard_delete(self, *args, **kwargs):
        self._validate_deletable()
        super().hard_delete(*args, **kwargs)


    def __str__(self):
        return f'({self.plate}) {self.brand} {self.model}'

