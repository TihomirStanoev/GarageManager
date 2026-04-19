from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cars.choices import BrandChoice, EngineChoice
from cars.models import Car
from common.models import RepairPartMixin
from repairs.choices import StatusChoice
from repairs.models import Repair

UserModel = get_user_model()


class RepairListViewTests(TestCase):
    def setUp(self):
        manager_group = Group.objects.get(name='Manager')
        self.manager = UserModel.objects.create_user(
            email='manager@manager.com',
            password='StrongPass123!',
            phone_number='+359888123456',
            first_name='Manager',
            last_name='Manager',
        )
        self.manager.groups.add(manager_group)

        car = Car.objects.create(
            brand=BrandChoice.BMW,
            model='Test',
            plate='CB1234AA',
            year=2020,
            engine_type=EngineChoice.GASOLINE,
            mileage=100_000,
        )

        self.repair = Repair.objects.create(
            category=RepairPartMixin.CategoryChoice.OTHER,
            car=car,
            status=StatusChoice.DRAFT,
        )

    def test_draft_repair_moves_to_in_progress_on_post(self):
        self.client.force_login(self.manager)
        self.client.post(
            path=reverse('repairs:repairs_list'),
            data={'repair_id': self.repair.pk})

        self.repair.refresh_from_db()


        self.assertEqual(self.repair.status, StatusChoice.IN_PROGRESS)