from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from books.views import (
	BookListAPIView,
	BookDetailsAPIView,
	BookCreateAPIView,
	BookDeleteAPIView,
)


app_name = "books"
base_url = "books"

urlpatterns = format_suffix_patterns(
	[
		path(f"{base_url}/", BookListAPIView.as_view(), name="books_list"),
		path(
			f"{base_url}/<int:pk>/", BookDetailsAPIView.as_view(), name="books_details"
		),
		# For admin purposes
		path(f"{base_url}/create/", BookCreateAPIView.as_view(), name="books_create"),
		path(
			f"{base_url}/delete/<int:pk>/",
			BookDeleteAPIView.as_view(),
			name="books_delete",
		),
	]
)
