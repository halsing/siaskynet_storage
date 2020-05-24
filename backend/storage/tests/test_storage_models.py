from django.test import TestCase

from storage.models import File
from users.models import CustomUser


class FileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@email.com", username="TestUser1", password="TestExmaple123445"
        )
        self.link = "sia://asdsadASFASDAFAasfasfasfaSAFFHFDH"
        self.name = "Test File"

    def test_create_file_valid(self):
        """ Test create new file"""
        file = File.objects.create(owner=self.user, file=self.link, name=self.name)

        self.assertEqual(file.name, self.name)
        self.assertEqual(file.file, self.link)
        self.assertEqual(
            file.generate_link(), "https://siasky.net/asdsadASFASDAFAasfasfasfaSAFFHFDH"
        )
