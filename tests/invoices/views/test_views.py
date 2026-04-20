from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from cars.choices import BrandChoice, EngineChoice
from cars.models import Car
from common.models import RepairPartMixin
from invoices.models import Invoice
from repairs.choices import StatusChoice
from repairs.models import Repair

UserModel = get_user_model()


class CreateInvoiceViewTests(TestCase):
    def setUp(self):
        manager_group = Group.objects.get(name='Manager')
        self.manager = UserModel.objects.create_user(
            email='manager@test.com',
            password='StrongPass123!',
            phone_number='+359888123456',
            first_name='Manager',
            last_name='Manager',
        )
        self.manager.groups.add(manager_group)

        self.owner = UserModel.objects.create_user(
            email='owner@test.com',
            password='StrongPass123!',
            phone_number='+359888654321',
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
            status=StatusChoice.COMPLETED,
            labor_hours=2,
            price_per_labor_hour=50,
        )

    @patch('invoices.views.send_mail_async.delay')
    def test_manager_post_creates_invoice_and_marks_repair_invoiced(self, mock_send_mail):
        self.client.force_login(self.manager)
        self.client.post(reverse('invoices:invoices_create', kwargs={'repair_pk': self.repair.pk}))

        self.repair.refresh_from_db()
        self.assertTrue(self.repair.is_invoiced)
        self.assertTrue(Invoice.objects.filter(repair=self.repair).exists())
