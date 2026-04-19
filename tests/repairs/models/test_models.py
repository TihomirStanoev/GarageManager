from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from cars.choices import BrandChoice, EngineChoice
from common.models import RepairPartMixin
from cars.models import Car
from repairs.choices import StatusChoice
from repairs.models import Repair, Part, RepairPart

UserModel = get_user_model()

class RepairModelTests(TestCase):
    def setUp(self):
        self.labor_hours = Decimal('5.0')
        self.price_per_labor_hour = Decimal('10.0')

        self.part_quantity = 5
        self.part_price = Decimal('15.0')

        self.category = RepairPartMixin.CategoryChoice.OTHER


        self.car = Car.objects.create(
            brand= BrandChoice.MERCEDES,
            model= 'WITH OWNER',
            plate='CB1237AA',
            year=2020,
            engine_type=EngineChoice.GASOLINE,
            mileage=100_000,
        )
        self.part = Part.objects.create(
            name='Test part',
            category=self.category,
            description='Test'
        )

        self.repair = Repair.objects.create(
            status=StatusChoice.COMPLETED,
            category=self.category,
            labor_hours = self.labor_hours,
            price_per_labor_hour=self.price_per_labor_hour,
            car=self.car,
        )

        self.repair_part = RepairPart.objects.create(
            repair=self.repair,
            part=self.part,
            quantity=self.part_quantity,
            price=self.part_price
        )


    def test_labor_price_returns_correct_value(self):
        labor_price_value = self.labor_hours * self.price_per_labor_hour

        self.assertEqual(self.repair.labor_price, labor_price_value)

    def test_part_price_returns_correct_value(self):
        part_price_value = self.part_quantity * self.part_price

        self.assertEqual(self.repair.parts_price, part_price_value)

    def test_total_price_returns_correct_value(self):
        labor_total = self.labor_hours * self.price_per_labor_hour
        part_total = self.part_price * self.part_quantity
        total_price = labor_total + part_total

        self.assertEqual(self.repair.total_price, total_price)

