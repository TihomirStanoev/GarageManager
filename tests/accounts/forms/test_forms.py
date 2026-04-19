from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import UpdateProfileForm

UserModel = get_user_model()


class UpdateProfileFormTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.com',
            password='testPass123!',
            phone_number='+359888123456',
            first_name='Firstname',
            last_name='Lastname',
        )

    def test_email_and_last_login_are_disabled(self):
        form = UpdateProfileForm(instance=self.user)

        for field in ('email', 'last_login'):
            with self.subTest(field=field):
                self.assertTrue(form.fields[field].disabled)


