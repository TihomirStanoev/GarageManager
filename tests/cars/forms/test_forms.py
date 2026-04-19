from django.test import TestCase

from cars.forms import UpdateCarForm
from cars.models import Car
from cars import choices

class UpdateCarFormTests(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            brand= choices.BrandChoice.BMW,
            model= 'TEST',
            plate='CB1234AA',
            year=2020,
            engine_type=choices.EngineChoice.GASOLINE,
            mileage=100_000,
        )

    def test_update_car_form_has_disabled_fields(self):
        form = UpdateCarForm(instance=self.car)

        for field in  ('brand', 'year', 'plate', 'engine_type', 'mileage'):
            with self.subTest(field=field):
                self.assertTrue(form.fields[field].disabled)




