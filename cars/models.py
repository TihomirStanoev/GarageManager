from django.db import models
from cars.choices import BrandChoice, EngineChoice
from cars.validators import ProductionYearValidator, PlateValidator
from common.models import TimeStampedModel


class Car(TimeStampedModel):
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

    image = models.ImageField(
        upload_to='cars/images',
        null=True, blank=True
    )

    owner = models.ForeignKey(
        to='profiles.Profile',
        on_delete=models.SET_NULL,
        related_name='cars',
        null=True, blank=True
    )

    class Meta:
        ordering = ['brand', 'model']

    def __str__(self):
        return f'({self.plate}) {self.brand} {self.model}'

