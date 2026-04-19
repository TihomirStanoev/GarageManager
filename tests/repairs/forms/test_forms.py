from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group
from cars.choices import BrandChoice, EngineChoice
from cars.models import Car
from common.models import RepairPartMixin
from repairs.choices import StatusChoice
from repairs.forms import UpdateRepairForm
from repairs.models import Repair

UserModel = get_user_model()

class RepairUpdateRepairFormTests(TestCase):
    def setUp(self):
        mechanic_group_name = 'Mechanic'
        mechanic_group = Group.objects.get(name=mechanic_group_name)
        car = Car.objects.create(
            brand= BrandChoice.MERCEDES,
            model= 'WITH OWNER',
            plate='CB1237AA',
            year=2020,
            engine_type=EngineChoice.GASOLINE,
            mileage=100_000,
        )

        self.data = {
            'description': 'Test',
            'labor_hours': '2.0',
            'price_per_labor_hour': '10.00',
            'status': StatusChoice.COMPLETED,
        }

        self.mechanic = UserModel.objects.create_user(
            email='mechanic@mechanic.com',
            password='PaszWodTest!',
            phone_number = '+359888123456',
            first_name='Mechanic',
            last_name='Mechanic'
        )
        self.mechanic.groups.add(mechanic_group)

        self.repair = Repair.objects.create(
            category=RepairPartMixin.CategoryChoice.OTHER,
            car=car,
        )


    def test_update_status_completed_without_mechanic_assert_error(self):
        form = UpdateRepairForm(
            data={**self.data,
                  'assigned_mechanics': [],
                  },
            instance=self.repair,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('assigned_mechanics', form.errors)


    def test_update_status_completed_with_mechanic_is_valid(self):
        form = UpdateRepairForm(
          data={**self.data,
              'assigned_mechanics': [self.mechanic.pk],
          },
          instance=self.repair,
        )
        self.assertTrue(form.is_valid())

