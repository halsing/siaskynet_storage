import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            "email": "test@email.com",
            "username": "TestUser",
            "password": "TestExample1234",
            "password2": "TestExample1234",
        }
        self.invalid_payload = {
            "email": "test@email.com",
            "username": "TestUser",
            "password": "TestExample1234",
            "password2": "TescIncorrect1234",
        }

    def test_registration_new_user_valid(self):
        response = self.client.post(
            reverse("registration_view"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_new_user_invalid(self):
        response = self.client.post(
            reverse("registration_view"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
