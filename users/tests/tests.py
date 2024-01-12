from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class UsersViewsTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse("users:user_register")
		self.login_url = reverse("users:user_login")
		self.refresh_token_url = reverse("users:user_token_refresh")
		self.user_url = reverse("users:user_retrieve_update")

		self.user_data = {
			"username": "testuser",
			"email": "testuser@example.com",
			"password": "testpassword123",
		}
		self.user = User.objects.create_user(**self.user_data)

		response = self.client.post(self.login_url, self.user_data, format="json")
		self.access_token = response.data["access"]
		self.refresh_token = response.data["refresh"]

	def test_registration_view(self):
		data = {
			"username": "newuser",
			"email": "newuser@example.com",
			"password": "newpassword123",
		}
		response = self.client.post(self.register_url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_login_view(self):
		data = {"email": "testuser@example.com", "password": "testpassword123"}
		response = self.client.post(self.login_url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("access", response.data)
		self.assertIn("refresh", response.data)

	def test_refresh_token_view(self):
		data = {"refresh": self.refresh_token}
		response = self.client.post(self.refresh_token_url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("access", response.data)

	def test_user_retrieve_view(self):
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
		response = self.client.get(self.user_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["username"], self.user.username)
		self.assertEqual(response.data["email"], self.user.email)

	def test_user_update_view(self):
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
		data = {"email": "newemail@example.com", "username": "newusername"}
		response = self.client.patch(self.user_url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["email"], data["email"])
		self.assertEqual(response.data["username"], data["username"])
