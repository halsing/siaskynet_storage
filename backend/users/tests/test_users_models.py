from django.test import TestCase

from users.models import CustomUser


class CustomUserTest(TestCase):
    """ Test for custom user model """

    def setUp(self):
        self.email = "test@email.com"
        self.password = "TestPasword1234"
        self.username = "TestUser"

    def test_create_user_valid(self):
        """ Test create new common user valid"""
        user = CustomUser.objects.create_user(email=self.email,username=self.username ,password=self.password)
        self.assertEqual(user.email, self.email, "Correct email")
        self.assertEqual(user.is_active, True)
        self.assertFalse(user.is_staff)

    def test_create_superuser_valid(self):
        """ Test create new superuser valid"""
        superuser = CustomUser.objects.create_superuser(
            email=self.email, username=self.username, password=self.password
        )

        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
