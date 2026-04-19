from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

UserModel = get_user_model()


class ProfileRegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')
        self.valid_data = {
            'email': 'new@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+359888123456',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }


    def test_register_with_valid_data_redirects(self):
        response = self.client.post(self.url, self.valid_data)
        target_url = reverse('home:index')

        self.assertRedirects(response, target_url)


class ProfileToggleStatusViewTests(TestCase):
    def setUp(self):
        self.manager_group = Group.objects.get(name='Manager')
        self.manager = UserModel.objects.create_user(
            email='manager@manager.com',
            first_name='Manager',
            last_name='Manager',
            phone_number='+359888123456',
            password='StrongPass123!',
        )
        self.manager.groups.add(self.manager_group)

        self.user = UserModel.objects.create_user(
                email='user@user.com',
                first_name='User',
                last_name='User',
                phone_number='+359888123458',
                password='StrongPass123!',
        )

    def test_manager_can_toggle_user_active_status(self):
        self.client.force_login(self.manager)

        self.client.post(reverse('accounts:toggle_active', kwargs={'pk': self.user.pk}))

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_non_manager_cannot_toggle_active_status(self):
        self.client.force_login(self.user)

        self.client.post(reverse('accounts:toggle_active', kwargs={'pk': self.manager.pk}))

        self.manager.refresh_from_db()
        self.assertTrue(self.manager.is_active)





class ProfileToggleRoleViewTests(TestCase):
    def setUp(self):
        self.manager_group_name = 'Manager'
        self.manager_group = Group.objects.get(name=self.manager_group_name)
        self.manager = UserModel.objects.create_user(
            email='manager@manager.com',
            first_name='Manager',
            last_name='Manager',
            phone_number='+359888123456',
            password='StrongPass123!',
        )
        self.manager.groups.add(self.manager_group)

        self.user = UserModel.objects.create_user(
                email='user@user.com',
                first_name='User',
                last_name='User',
                phone_number='+359888123458',
                password='StrongPass123!',
        )

    def test_manager_can_assign_role_to_user(self):
        self.client.force_login(self.manager)

        self.client.post(
            path=reverse('accounts:toggle_role', kwargs={'pk': self.user.pk}),
            data={'role': self.manager_group_name}
        )

        self.assertIn(self.manager_group, self.user.groups.all())


