from rest_framework.generics import (
	DestroyAPIView,
	RetrieveAPIView,
	ListAPIView,
	CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from books.models import Book
from books.serializers import (
	BookListSerializer,
	BookDetailsSerializer,
	BookCreateSerializer,
	BookDeleteSerializer,
)


class BookListAPIView(ListAPIView):
	"""
	List all books with its info.

	Methods:
	    - GET: retrieve all books.

	Endpoints:
	    /books/

	Response:
	    {
	        "id": id,
	        "author": str,
	        "name": str,
	        "publish_year": int,
	        "short_description": str,
	        "readers": int
	    }, ...
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = BookListSerializer
	queryset = Book.objects.all()


class BookCreateAPIView(CreateAPIView):
	"""
	Create a book.

	Methods:
	    - POST: retrieve all books.

	Endpoints:
	    /books/create/

	Body:
	    {
	        "author": str,
	        "name": str,
	        "publish_year": int,
	        "short_description": str,
	        "full_description": str
	    }
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = BookCreateSerializer


class BookDetailsAPIView(RetrieveAPIView):
	"""
	List book details by id.

	Methods:
	    - GET: retrieve a book detailed info, pk is required.

	Endpoints:
	    /books/<int:pk>/

	Response:
	    {
	        "id": id,
	        "author": str,
	        "name": str,
	        "publish_year": int,
	        "short_description": str,
	        "full_description": str,
	        "readers": int
	    }
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = BookDetailsSerializer
	queryset = Book.objects.all()


class BookDeleteAPIView(DestroyAPIView):
	"""
	DELETE.
	Delete a book by id. Only for admins.

	Methods:
	    - DELETE: delete a book by id, pk is required.

	Endpoints:
	    /books/delete/<int:pk>/
	"""

	permission_classes = (IsAdminUser,)
	serializer_class = BookDeleteSerializer
	queryset = Book.objects.all()
