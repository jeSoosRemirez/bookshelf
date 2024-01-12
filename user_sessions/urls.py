from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user_sessions.views import (
	UserSessionDetailsListAPIView,
	UserSessionListAPIView,
	SessionStartAPIView,
	UserSessionCreateAPIView,
	UserSessionDeleteAPIView,
	UserSessionListAllAPIView,
	UserSessionDetailsAPIView,
)


app_name = "user_sessions"
base_url = "books"

urlpatterns = format_suffix_patterns(
	[
		path(
			f"{base_url}/sessions/", UserSessionListAPIView.as_view(), name="sessions"
		),
		path(
			f"{base_url}/<int:pk>/sessions/",
			UserSessionListAPIView.as_view(),
			name="sessions_book",
		),
		path(
			f"{base_url}/sessions/detailed/",
			UserSessionDetailsListAPIView.as_view(),
			name="sessions_detailed",
		),
		path(
			f"{base_url}/<int:pk>/sessions/detailed/",
			UserSessionDetailsListAPIView.as_view(),
			name="sessions_detailed_book",
		),
		path(
			f"{base_url}/<int:pk>/sessions/start_end/",
			SessionStartAPIView.as_view(),
			name="sessions_start_end",
		),
		# For admin purposes
		path(
			f"{base_url}/sessions/all/",
			UserSessionListAllAPIView.as_view(),
			name="sessions_all",
		),
		path(
			f"{base_url}/sessions/<int:pk>/",
			UserSessionDetailsAPIView.as_view(),
			name="sessions_all_detailed",
		),
		path(
			f"{base_url}/sessions/create/",
			UserSessionCreateAPIView.as_view(),
			name="sessions_create",
		),
		path(
			f"{base_url}/sessions/delete/<int:pk>/",
			UserSessionDeleteAPIView.as_view(),
			name="sessions_delete",
		),
	]
)
