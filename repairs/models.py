import random
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from cars.models import Car
from common.models import RepairPartMixin, TimeStampedModel
from repairs.choices import StatusChoice


class Part(RepairPartMixin):
    name = models.CharField(
        max_length=50
    )

    image = models.ImageField(
        upload_to='parts/images',
        null=True, blank=True
    )


    def __str__(self):
        return f'{self.name}'



class Repair(RepairPartMixin):
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

    def __str__(self):
        return f'{self.category} - {self.status}'


    @property
    def labor_price(self):
        return self.labor_hours * self.price_per_labor_hour

    @property
    def parts_price(self):
        return sum(pe.parts_price for pe in self.part_entries.all())

    @property
    def total_price(self):
        return self.labor_price + self.parts_price





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



class Invoice(TimeStampedModel):
    invoice_number = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    repair = models.ForeignKey(
        to='Repair',
        on_delete=models.CASCADE,
        related_name='invoices')

    owner = models.ForeignKey(
        to='profiles.Profile',
        on_delete=models.SET_NULL,
        related_name='invoices',
        null=True, blank=True
    )


    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(limit_value=Decimal('0.00'), message=f'Total amount cannot be negative.')]
    )

    class Meta:
        ordering = ['-created_at']


    def _generate_invoice_number(self):
        while True:
            unique_ref = str(random.randint(1000000000, 9999999999))
            if not Invoice.objects.filter(invoice_number=unique_ref): break
        return unique_ref


    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()

        if not self.owner_id:
            self.owner = self.repair.car.owner

        if not self.total_amount:
            self.total_amount = self.repair.total_price


        super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.owner} ({self.repair.car}) - {self.invoice_number}'