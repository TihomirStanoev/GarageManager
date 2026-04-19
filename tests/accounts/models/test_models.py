from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.validators import PhoneNumberValidator

UserModel = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.com',
            password='testPawss3rd',
            phone_number='+359888888888',
            first_name='Firstname',
            last_name='Lastname',
        )

    def test_first_name_strips_whitespace(self):
        self.user.first_name = '  Firstname  '
        self.user.save()
        self.assertEqual(self.user.first_name, 'Firstname')


    def test_first_name_capitalizes(self):
        self.user.first_name = 'firstname'
        self.user.save()
        self.assertEqual(self.user.first_name, 'Firstname')


    def test_last_name_strips_whitespace(self):
        self.user.last_name = '  Lastname  '
        self.user.save()
        self.assertEqual(self.user.last_name, 'Lastname')

    def test_last_name_capitalizes(self):
        self.user.last_name = 'lastname'
        self.user.save()
        self.assertEqual(self.user.last_name, 'Lastname')


    def test_empty_first_name_does_not_crash(self):
        self.user.first_name = ''
        self.user.save()
        self.assertEqual(self.user.first_name, '')


    def test_profile_with_phone_property(self):
        expected = f'{self.user.first_name} {self.user.last_name} ({self.user.phone_number})'
        self.assertEqual(self.user.profile_with_phone, expected)



class PhoneNumberValidatorTests(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator()

    valid_numbers = [
        '+359888123456',
        '+359123456789',
    ]

    invalid_numbers = [
        '359888123456',
        '+44888123456',
        '+35912345678',
        '+3591234567890',
        '+359abc123456',
        '',
        '+359 888 123 456',]

    def test_valid_numbers(self):
        for number in self.valid_numbers:
            with self.subTest(number=number):
                self.assertIsNone(self.validator(number))

    def test_invalid_numbers(self):
        for number in self.invalid_numbers:
            with self.subTest(number=number):
                with self.assertRaises(ValidationError):
                    self.validator(number)