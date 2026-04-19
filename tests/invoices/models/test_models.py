from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from cars.choices import BrandChoice, EngineChoice
from cars.models import Car
from common.models import RepairPartMixin
from invoices.models import Invoice
from repairs.choices import StatusChoice
from repairs.models import Repair

UserModel = get_user_model()


class InvoiceCleanTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            email='owner@test.com',
            password='StrongPass123!',
            phone_number='+359888123456',
            first_name='Owner',
            last_name='Owner',
        )

        self.car = Car.objects.create(
            brand=BrandChoice.BMW,
            model='Test',
            plate='CB1234AA',
            year=2020,
            engine_type=EngineChoice.GASOLINE,
            mileage=100_000,
            owner=self.owner,
        )

        self.repair = Repair.objects.create(
            category=RepairPartMixin.CategoryChoice.OTHER,
            car=self.car,
            status=StatusChoice.DRAFT,
        )

        self.invoices = Invoice.objects.create(
            repair=self.repair,
            owner=self.owner,
            total_amount=Decimal('50.00')
        )

    def test_invoice_clean_raises_validation_error_when_repair_not_completed(self):
        expected_message = 'Cannot invoice a repair that is not yet completed.'

        with self.assertRaises(ValidationError) as e:
            self.invoices.full_clean()

        exception = e.exception

        self.assertIn(expected_message, exception.messages)


    def test_create_invoice_with_completed_repair_does_not_raise(self):
        self.repair.status = StatusChoice.COMPLETED
        self.repair.save()

        try:
            self.invoices.full_clean()
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly.')
