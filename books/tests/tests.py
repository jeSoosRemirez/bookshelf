from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse
from books.models import Book


class BooksViewsTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.book_list_url = reverse("books:books_list")
		self.book_create_url = reverse("books:books_create")
		self.book_details_url = reverse("books:books_details", args=[1])
		self.book_delete_url = reverse("books:books_delete", args=[1])

		self.user_data = {
			"username": "testuser",
			"email": "testuser@example.com",
			"password": "testpassword123",
		}
		self.user = User.objects.create_user(**self.user_data)
		self.client.force_authenticate(user=self.user)

		self.book_data = {
			"author": "Test Author",
			"name": "Test Book",
			"publish_year": 2022,
			"short_description": "Short description",
			"full_description": "Full description",
		}
		self.book = Book.objects.create(**self.book_data)

	def test_book_list_view(self):
		response = self.client.get(self.book_list_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_book_create_view(self):
		admin_user = User.objects.create_superuser(
			"admin", "admin@example.com", "adminpassword123"
		)
		self.client.force_authenticate(user=admin_user)

		data = {
			"author": "New Author",
			"name": "New Book",
			"publish_year": 2023,
			"short_description": "New Short description",
			"full_description": "New Full description",
		}
		response = self.client.post(self.book_create_url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_book_details_view(self):
		response = self.client.get(self.book_details_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_book_delete_view(self):
		admin_user = User.objects.create_superuser(
			"admin", "admin@example.com", "adminpassword123"
		)
		self.client.force_authenticate(user=admin_user)

		response = self.client.delete(self.book_delete_url, format="json")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
