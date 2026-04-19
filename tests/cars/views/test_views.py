from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cars import choices
from cars.models import Car


UserModel = get_user_model()

class CarListViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            email='test@test.com',
            password='testPawss3rd',
            phone_number='+359888888888',
            first_name='Firstname',
            last_name='Lastname',
        )

        self.car_with_owner = Car.objects.create(
            brand= choices.BrandChoice.MERCEDES,
            model= 'WITH OWNER',
            plate='CB1237AA',
            year=2020,
            engine_type=choices.EngineChoice.GASOLINE,
            mileage=100_000,
            owner=self.owner
        )

        self.car_wo_owner = Car.objects.create(
            brand= choices.BrandChoice.BMW,
            model= 'WITHOUT OWNER',
            plate='CB1234AA',
            year=2020,
            engine_type=choices.EngineChoice.GASOLINE,
            mileage=100_000,
        )


    def test_regular_user_sees_only_their_own_cars(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse('cars:list'))

        owner_cars = response.context.get('cars')

        self.assertNotIn(
            member=self.car_wo_owner,
            container=owner_cars
        )

