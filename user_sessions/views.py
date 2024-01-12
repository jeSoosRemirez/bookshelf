from datetime import datetime
from django.db.models import F, ExpressionWrapper, Sum, fields
from rest_framework import status
from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveAPIView,
	UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from user_sessions.models import UserSession
from user_sessions.serializers import (
	UserSessionListSerializerAPIView,
	UserSessionDetailsSerializer,
	UserSessionCreateSerializer,
	UserSessionDeleteSerializer,
	UserSessionListAllSerializerAPIView,
)


class UserSessionDetailsListAPIView(ListAPIView):
	"""
	List a detailed sessions info for curr user.
	If primary key of a book was provided it will show
	a data for an exact book, otherwise for all books.

	Methods:
	    - GET: If pk, retrieve data for a book;
	    if not pk, retrieve data for all books.

	Endpoints:
	    /books/sessions/detailed/
	    /books/<int:pk>/sessions/detailed/

	Response:
	    {
	        "id": id,
	        "user": pk,
	        "book": pk,
	        "sessions_start": datetime,
	        "session_end": datetime,
	        "elapsed_time": datetime
	    }
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = UserSessionDetailsSerializer

	def get_queryset(self):
		if "pk" in self.kwargs:
			return UserSession.objects.all().filter(
				user=self.request.user, book=self.kwargs["pk"]
			)
		return UserSession.objects.all().filter(user=self.request.user)


class UserSessionListAPIView(ListAPIView):
	"""
	List total elapsed time for all books or an exact book.
	If primary key of a book was provided it will show
	a data for an exact book, otherwise for all books.

	Methods:
	    - GET: If pk, retrieve time for a book;
	    if not pk, retrieve time for all books.

	Endpoints:
	    /books/sessions/
	    /books/<int:pk>/sessions/

	Response:
	    {
	        "book": pk,
	        "total_elapsed_time": datetime
	    }
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = UserSessionListSerializerAPIView

	def get_queryset(self):
		if "pk" in self.kwargs:
			return UserSession.objects.all().filter(
				user=self.request.user, book=self.kwargs["pk"]
			)
		return UserSession.objects.all().filter(user=self.request.user)

	def get(self, request, pk=None):
		# Aggregate the sum of elapsed_time for each book
		queryset = self.get_queryset()
		user_sessions = (
			queryset.annotate(
				elapsed_time=ExpressionWrapper(
					F("session_end") - F("session_start"),
					output_field=fields.DurationField(),
				)
			)
			.values("book")
			.annotate(total_elapsed_time=Sum("elapsed_time"))
		)

		serialized_data = []
		for data in user_sessions:
			book_id = data["book"]
			total_elapsed_time = data["total_elapsed_time"]
			serialized_data.append(
				{
					"book": book_id,
					"total_elapsed_time": str(total_elapsed_time),
				}
			)
		return Response(serialized_data)


class SessionStartAPIView(CreateAPIView, UpdateAPIView):
	"""
	Start and end session for curr user for a book. POST will
	create a record and set session_start, PATCH will actualy
	add session_end to EVERY record that are without session_end.

	Methods:
	    - POST: Start a session with a book;
	    - PATCH: End a session with a book. The session going to auto-end
	    if another session has started and a previous one was not ended.

	Endpoints:
	    /books/<int:pk>/sessions/start_end/

	Response:
	    - POST:
	    {
	        "user": pk,
	        "book": pk,
	        "sessions_start": datetime,
	        "session_end": null
	    }
	    - PATCH:
	    only status 200
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = UserSessionCreateSerializer

	def get_queryset(self):
		return UserSession.objects.all().filter(user=self.request.user)

	def post(self, request, pk=None):
		if self.get_queryset().filter(session_end=None):
			self.update(request)
		user = request.user.pk
		data = {"user": user, "book": pk}
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def update(self, request, partial=True, pk=None):
		queryset = self.get_queryset().filter(session_end=None)
		queryset.update(session_end=datetime.now())
		return Response(status=status.HTTP_200_OK)


class UserSessionCreateAPIView(CreateAPIView):
	"""
	Create a session. Only for admin purposes.

	Endpoints:
	    /books/sessions/create/

	Methods:
	    - POST: Create a session record. Args:
	        {
	            "user": pk,
	            "book": pk,
	            "session_start": datetime,
	            "session_end": datetime
	        }
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = UserSessionCreateSerializer


class UserSessionListAllAPIView(ListAPIView):
	"""
	Retrieve all session records.
	Only for admin purposes.

	Endpoints:
	    /books/sessions/all/

	Methods:
	    - GET: Retrieve all session records.

	Response:
	    {
	        "id": pk,
	        "user": pk,
	        "book": pk,
	        "session_start": datetime,
	        "session_end": datetime,
	        "elapsed_time": datetime
	    }, ...
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = UserSessionListAllSerializerAPIView
	queryset = UserSession.objects.all()


class UserSessionDetailsAPIView(RetrieveAPIView):
	"""
	Retrieve session data by id.
	Only for admin purposes.

	Endpoints:
	    /books/sessions/<int:pk>/

	Methods:
	    - GET: Retrieve a session record, pk should be provided in url.

	Response:
	    {
	        "id": pk,
	        "user": pk,
	        "book": pk,
	        "session_start": datetime,
	        "session_end": datetime,
	        "elapsed_time": datetime
	    }
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = UserSessionDetailsSerializer
	queryset = UserSession.objects.all()


# Delete record
class UserSessionDeleteAPIView(DestroyAPIView):
	"""
	Delete session record by id. Only for admin purposes.

	Endpoints:
	    /books/sessions/delete/<int:pk>/

	Methods:
	    - DELETE: Delete a session record, pk should be provided in url.
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = UserSessionDeleteSerializer
	queryset = UserSession.objects.all()
