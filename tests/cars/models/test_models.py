from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from cars import choices
from cars.models import Car

UserModel = get_user_model()

class CarModelTests(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            brand= choices.BrandChoice.BMW,
            model= 'TEST',
            plate='CB1234AA',
            year=2020,
            engine_type=choices.EngineChoice.GASOLINE,
            mileage=100_000,
        )


    def test_delete_car_with_owner_raises_validation_error(self):
        expected_message = 'Cannot delete car: cannot delete a car that has an owner assigned..'
        user = UserModel.objects.create_user(
            email='test@test.com',
            password='testPass123!',
            phone_number='+359888123456',
            first_name='Firstname',
            last_name='Lastname',
        )
        self.car.owner = user
        self.car.save()

        with self.assertRaises(ValidationError) as e:
            self.car.delete()

        exception = e.exception
        self.assertEqual(first=expected_message,
                         second=exception.message)


    def test_car_soft_deletion(self):
        self.car.delete()
        self.assertTrue(self.car.is_deleted)