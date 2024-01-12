from django.urls import path
from users.views import (
	LoginAPIView,
	RefreshTokenAPIView,
	RegistrationAPIView,
	UserRetrieveUpdateAPIView,
)


app_name = "users"
base_url = "users"

urlpatterns = [
	# user list
	path(
		f"{base_url}/", UserRetrieveUpdateAPIView.as_view(), name="user_retrieve_update"
	),
	path(f"{base_url}/register/", RegistrationAPIView.as_view(), name="user_register"),
	path(f"{base_url}/login/", LoginAPIView.as_view(), name="user_login"),
	path(
		f"{base_url}/login/refresh/",
		RefreshTokenAPIView.as_view(),
		name="user_token_refresh",
	),
]
