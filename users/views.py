from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.serializers import RegistrationSerializer, UserSerializer


class RegistrationAPIView(APIView):
	"""
	Register a user.

	Methods:
	    - POST: create a user.

	Endpoints:
	    /users/register/

	Body:
	{
	    "username": str,
	    "email": str,
	    "password": str(>=8)
	}

	Response:
	    {"email": str, "username": str}
	"""

	permission_classes = (AllowAny,)
	serializer_class = RegistrationSerializer

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
	"""
	Login a user. Retrieve access_token and refresh_token.

	Methods:
	    - POST: login to retrieve tokens.

	Endpoints:
	    /users/login/

	Body:
	{"email": str, "password": str}

	Response:
	    {"refresh": refresh_token, "access": access_token}
	"""

	permission_classes = (AllowAny,)


class RefreshTokenAPIView(TokenRefreshView):
	"""
	Update access_token by refresh_token.

	Methods:
	    - POST: retrieve new refresh_token.

	Endpoints:
	    /users/login/refresh/

	Body:
	    {"refresh": refresh_token}

	Response:
	    {"access": new_access_token}
	"""

	permission_classes = (AllowAny,)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
	"""
	Retrieve user details or update user info.

	Methods:
	    - GET: retrieve curr user info;
	    - PATCH: update curr user info.

	Endpoints:
	    /users/

	More info in methods...
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = UserSerializer

	def retrieve(self, request, *args, **kwargs):
		"""
		Retrieve user details.

		Response:
		    dict: {"email": str, "username": str, "session_stats": dict}
		"""
		serializer = self.serializer_class(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		"""
		Update user data.

		Body:
			{"email: "new_email", "username": "new_username"}.
		    data can consist of only "email", or only "username", or both.

		Response:
		    {"email": str, "username": str}
		"""
		serializer_data = request.data

		serializer = self.serializer_class(
			request.user, data=serializer_data, partial=True
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)
