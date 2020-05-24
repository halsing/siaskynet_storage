# from django.urls import reverse
# from unittest.mock import patch
# from rest_framework.test import (
#     APIClient,
#     APITestCase,
#     APIRequestFactory,
#     force_authenticate,
# )
# from rest_framework import status

# from storage.models import File
# from storage.api.views import FileView
# from users.models import CustomUser

# from storage.tests.helpers import temp_image


# class CreateFileTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.email = "Test@test.pl"
#         self.password = "TestPassword1234"
#         self.test_name = "Test image name"

#         self.user = CustomUser.objects.create_user(
#             email=self.email, password=self.password
#         )

#         token = self.client.post(
#             reverse("token_obtain_pair"),
#             {"email": self.email, "password": self.password},
#             format="json",
#         )
#         token_access = token.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_access}")

#     def test_get_user_files_list_valid(self):

#         response = self.client.get("/api/storage/files/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     @patch("siaskynet.Skynet.UploadFile")
#     def test_create_new_file_valid(self, mock_get):
#         mock_get.return_value = "sia://TestLink"
#         temp_file = temp_image()

#         response = self.client.post(
#             reverse("file-list"),
#             {"file": temp_file, "name": self.test_name},
#             format="multipart",
#         )

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["file"], "sia://TestLink")
#         self.assertEqual(len(File.objects.all()), 1)
#         self.assertEqual(File.objects.all()[0].file, "sia://TestLink")


# class DeleteFileTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.email = "Test@test.pl"
#         self.password = "TestPassword1234"
#         self.test_name = "Test image name"
#         self.link = "sia://asdsadASFASDAFAasfasfasfaSAFFHFDH"
#         self.name = "Test File"
#         self.user = CustomUser.objects.create_user(
#             email=self.email, password=self.password
#         )

#         self.file = File.objects.create(owner=self.user, file=self.link, name=self.name)

#         self.token = self.client.post(
#             reverse("token_obtain_pair"),
#             {"email": self.email, "password": self.password},
#             format="json",
#         )

#     def test_delete_file_valid(self):

#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.data['access']}")
#         response = self.client.delete(
#             f"/api/storage/files/{self.file.id}/", format="json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# # class GetOnlyUserFiles(APITestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.first_link = "sia://TestFirst"
# #         self.second_link = "sia://TestSecond"
# #         self.first_payload = {
# #             "email": "test1@gmail.com",
# #             "password": "Test123456"
# #         }
# #         self.second_payload = {
# #             "email": "test2@gmail.com",
# #             "password": "Test123456"
# #         }

# #         self.first_user = CustomUser.objects.create_user(**self.first_payload)
# #         self.second_user = CustomUser.objects.create_user(**self.second_payload)

# #         self.first_file = File.objects.create(
# #             owner=self.first_user,
# #             file=self.first_link,
# #             name="Test first name"
# #         )

# #         self.second_file = File.objects.create(
# #             owner=self.second_user,
# #             file=self.second_link,
# #             name="Test second name"
# #         )

# #     def test_user_get_owned_objects(self):

# #         response = self.client.get("/api/storage/files/")

# #         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class GoodTest(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = CustomUser.objects.create_user(
#             email="test1@gmail.com", password="Test123456"
#         )

#     def test_get(self):
#         view = FileView.as_view({"get": "list"})
#         request = self.factory.get("/api/storage/files/")
#         force_authenticate(request, user=self.user)
#         response = view(request)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
