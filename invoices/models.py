from decimal import Decimal
import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from repairs.choices import StatusChoice
from common.models import TimeStampedModel
from repairs.models import Repair


class Invoice(TimeStampedModel):
    invoice_number = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    repair = models.OneToOneField(
        to=Repair,
        on_delete=models.PROTECT,
        related_name='invoice')

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='invoices',
    )


    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=Decimal('0.01'), message=f'Total amount cannot be negative.')]
    )

    class Meta:
        ordering = ['-created_at']


    def _generate_invoice_number(self):
        while True:
            unique_ref = str(random.randint(1000000000, 9999999999))
            if not Invoice.objects.filter(invoice_number=unique_ref): break
        return unique_ref


    def clean(self):
        super().clean()

        if self.repair.status != StatusChoice.COMPLETED:
            raise ValidationError('Cannot invoice a repair that is not yet completed.')



    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()

        if not self.owner_id:
            if not self.repair.car.owner:
                raise ValidationError('Cannot create invoice for a car without an owner.')
            self.owner = self.repair.car.owner

        if not self.total_amount:
            self.total_amount = self.repair.total_price


        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.owner} ({self.repair.car}) - {self.invoice_number}'