from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from books.models import Book
from django.urls import reverse
from user_sessions.models import UserSession
from datetime import datetime, timedelta


class UserSessionsViewsTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			username="testuser", password="testpassword123", email="test@mail.com"
		)
		self.client.force_authenticate(user=self.user)
		self.book_data = {
			"author": "Test Author",
			"name": "Test Book",
			"publish_year": 2022,
			"short_description": "Short description",
			"full_description": "Full description",
		}
		self.book = Book.objects.create(**self.book_data)
		self.user_session_data = {
			"user": self.user,
			"book": self.book,
			"session_start": datetime.now(),
		}
		self.user_session = UserSession.objects.create(**self.user_session_data)
		self.user_sessions_list_url = reverse("user_sessions:sessions")
		self.user_sessions_details_list_url = reverse("user_sessions:sessions_detailed")
		self.user_sessions_details_list_book_url = reverse(
			"user_sessions:sessions_detailed_book", args=[self.book.id]
		)
		self.session_start_end_url = reverse(
			"user_sessions:sessions_start_end", args=[self.book.id]
		)
		self.admin_user = User.objects.create_superuser(
			"admin", "admin@example.com", "adminpassword123"
		)

	def test_user_session_list_view(self):
		response = self.client.get(self.user_sessions_list_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_session_details_list_view(self):
		response = self.client.get(self.user_sessions_details_list_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_session_details_list_book_view(self):
		response = self.client.get(
			self.user_sessions_details_list_book_url, format="json"
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_session_start_end_view(self):
		import time

		time.sleep(2)

		response_start = self.client.post(self.session_start_end_url, format="json")
		self.assertEqual(response_start.status_code, status.HTTP_201_CREATED)

		self.assertIsNone(response_start.data.get("elapsed_time"))

		time.sleep(2)

		response_end = self.client.patch(self.session_start_end_url, format="json")
		self.assertEqual(response_end.status_code, status.HTTP_200_OK)

		if response_end.data is not None:
			self.assertIn("elapsed_time", response_end.data)
			elapsed_time = response_end.data.get("elapsed_time")
			self.assertGreater(elapsed_time, timedelta(minutes=0))
		else:
			self.fail("response_end.data is None")

	def test_user_session_create_view(self):
		self.client.force_authenticate(user=self.admin_user)
		data = {
			"user": self.user.id,
			"book": self.book.id,
			"session_start": datetime.now(),
			"session_end": datetime.now() + timedelta(minutes=30),
		}
		response = self.client.post(
			reverse("user_sessions:sessions_create"), data, format="json"
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_user_session_list_all_view(self):
		self.client.force_authenticate(user=self.admin_user)
		response = self.client.get(reverse("user_sessions:sessions_all"), format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_session_details_view(self):
		self.client.force_authenticate(user=self.admin_user)
		response = self.client.get(
			reverse("user_sessions:sessions_all_detailed", args=[self.user_session.id]),
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_session_delete_view(self):
		self.client.force_authenticate(user=self.admin_user)
		response = self.client.delete(
			reverse("user_sessions:sessions_delete", args=[self.user_session.id]),
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
