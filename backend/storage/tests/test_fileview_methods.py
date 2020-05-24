from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from storage.models import File
from storage.api.views import FileView
from users.models import CustomUser

from storage.tests.helpers import temp_image


class ListFileTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_first = CustomUser.objects.create_user(
            email="test1@gmail.com", username="TestUser1", password="Test123456"
        )
        self.user_second = CustomUser.objects.create_user(
            email="test2@gmail.com", username="TestUser2", password="Test123456"
        )
        self.view = FileView.as_view({"get": "list"})
        url = reverse("file-list")
        self.request = self.factory.get(url)

    def test_401_for_not_authenticated_user(self):
        response = self.view(self.request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_200_for_authenticated_user(self):
        force_authenticate(self.request, user=self.user_first)
        response = self.view(self.request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_files_only_current_user(self):
        File.objects.create(
            owner=self.user_first, file="sia://TestFirst", name="Test first"
        )
        File.objects.create(
            owner=self.user_second, file="sia://TestSecond", name="Test second"
        )

        force_authenticate(self.request, user=self.user_first)
        response = self.view(self.request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["owner"], self.user_first.email)
        self.assertTrue("sia://TestFirst" in response.data[0].values())

        self.assertFalse(self.user_second.email in response.data[0].values())
        self.assertFalse("sia://TestSecond" in response.data[0].values())


class RetrieveFileTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_first = CustomUser.objects.create_user(
            email="test1@gmail.com", username="TestUser1", password="Test123456"
        )
        self.user_second = CustomUser.objects.create_user(
            email="test2@gmail.com", username="TestUser2", password="Test123456"
        )

        self.file_first = File.objects.create(
            owner=self.user_first, file="sia://TestFirst", name="Test first"
        )
        self.file_second = File.objects.create(
            owner=self.user_second, file="sia://TestSecond", name="Test second"
        )

    def test_200_for_owned_object(self):
        view = FileView.as_view({"get": "retrieve"})
        file_id = self.file_first.id
        url = reverse("file-detail", args=[file_id])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user_first)
        response = view(request, pk=file_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_401_for_not_authenticated_user(self):
        view = FileView.as_view({"get": "retrieve"})
        file_id = self.file_second.id
        url = reverse("file-detail", args=[file_id])
        request = self.factory.get(url)
        response = view(request, pk=file_id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_404_for_not_owned_object(self):
        view = FileView.as_view({"get": "retrieve"})
        file_id = self.file_second.id
        request = self.factory.get("/api/storage/files/")
        force_authenticate(request, user=self.user_first)
        response = view(request, pk=file_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateFileTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(
            email="test1@gmail.com", username="TestUser1", password="Test123456"
        )

    @patch("siaskynet.Skynet.UploadFile")
    def test_201_for_create_file(self, mock_get):
        mock_get.return_value = "sia://TestLink"
        view = FileView.as_view({"post": "create"})
        url = reverse("file-list")
        request = self.factory.post(
            url, {"file": temp_image(), "name": "Test name"}, format="multipart",
        )

        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("siaskynet.Skynet.UploadFile")
    def test_401_create_file_by_anonymous_user(self, mock_get):
        mock_get.return_value = "sia://TestLink"
        view = FileView.as_view({"post": "create"})
        url = reverse("file-list")
        request = self.factory.post(
            url, {"file": temp_image(), "name": "Test name"}, format="multipart",
        )
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteFile(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_first = CustomUser.objects.create_user(
            email="test1@gmail.com", username="TestUser1", password="Test123456"
        )
        self.user_second = CustomUser.objects.create_user(
            email="test2@gmail.com", username="TestUser2", password="Test123456"
        )

        self.file_first = File.objects.create(
            owner=self.user_first, file="sia://TestFirst", name="Test first"
        )
        self.file_second = File.objects.create(
            owner=self.user_second, file="sia://TestSecond", name="Test second"
        )

    def test_204_delete_owned_object(self):
        file_id = self.file_first.id
        view = FileView.as_view({"delete": "destroy"})
        url = reverse("file-detail", args=[file_id])
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user_first)
        response = view(request, pk=file_id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_401_delete_anonymous_user(self):
        file_id = self.file_first.id
        view = FileView.as_view({"delete": "destroy"})
        url = reverse("file-detail", args=[file_id])
        request = self.factory.delete(url)
        response = view(request, pk=file_id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
