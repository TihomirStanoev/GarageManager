from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from common.managers import SoftDeleteManager
from common.models import RepairPartMixin, TimeStampedModel, SoftDeletionMixin
from repairs.choices import StatusChoice
from django.conf import settings


class Part(SoftDeletionMixin, RepairPartMixin):
    name = models.CharField(
        max_length=50
    )

    image = models.ImageField(
        upload_to='parts/images',
        null=True, blank=True
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return f'{self.name}'



class Repair(SoftDeletionMixin, RepairPartMixin):
    DEFAULT_LABOR_PRICE = Decimal('0.00')


    status = models.CharField(
        max_length=40,
        choices=StatusChoice.choices,
        default=StatusChoice.DRAFT,
    )

    labor_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal('0.0'),
        validators=[
            MinValueValidator(limit_value=Decimal('0.0'), message=f'Labor hours cannot be negative.')]
    )

    price_per_labor_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=DEFAULT_LABOR_PRICE,
        validators=[
            MinValueValidator(limit_value=Decimal('0.00'), message=f'Hourly rate cannot be negative.')
        ]
    )

    car = models.ForeignKey(
        to='cars.Car',
        on_delete=models.CASCADE,
        related_name='repairs'
    )

    parts = models.ManyToManyField(
        to='Part',
        through='RepairPart',
        related_name='repairs'
    )

    is_invoiced = models.BooleanField(default=False)

    assigned_mechanics = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='assigned_repairs',
        blank=True
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        permissions = [
            ('change_repair_status', 'Can change repair status'),
            ('change_repair_mechanic', 'Can change mechanic')
        ]

    def _validate_deletable(self):
        if self.is_invoiced:
            raise ValidationError('Cannot delete repair: an invoice has already been issued.')


    def delete(self, *args, **kwargs):
        self._validate_deletable()
        super().delete(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        self._validate_deletable()
        super().hard_delete(*args, **kwargs)


    @property
    def labor_price(self):
        return self.labor_hours * self.price_per_labor_hour

    @property
    def parts_price(self):
        return sum(pe.parts_price for pe in self.part_entries.all())

    @property
    def total_price(self):
        return self.labor_price + self.parts_price

    def __str__(self):
        return f'{self.car.plate} - {self.car.owner.profile_with_phone} - {self.total_price:.2f}'





class RepairPart(TimeStampedModel):
    repair = models.ForeignKey(
        to='Repair',
        on_delete=models.CASCADE,
        related_name='part_entries')

    part = models.ForeignKey(
        to='Part',
        on_delete=models.CASCADE,
        related_name='repair_entries')

    quantity = models.PositiveIntegerField(
        default=1,)

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(limit_value=Decimal('0.00'), message=f'Price cannot be negative.')]
    )

    class Meta:
        unique_together = ['repair', 'part']


    @property
    def parts_price(self):
        return self.price * self.quantity


    def __str__(self):
        return f'{self.part} - {self.quantity}'



