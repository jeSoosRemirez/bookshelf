from rest_framework import serializers
from books.models import Book


class BookListSerializer(serializers.ModelSerializer):
	readers = serializers.SerializerMethodField()

	class Meta:
		model = Book
		fields = [
			"id",
			"author",
			"name",
			"publish_year",
			"short_description",
			"readers",
		]

	def get_readers(self, obj):
		return obj.readers.count()


class BookCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = [
			"id",
			"author",
			"name",
			"publish_year",
			"short_description",
			"full_description",
			"readers",
		]
		extra_kwargs = {"readers": {"read_only": True}}


class BookDetailsSerializer(serializers.ModelSerializer):
	readers = serializers.SerializerMethodField()

	class Meta:
		model = Book
		fields = [
			"id",
			"author",
			"name",
			"publish_year",
			"short_description",
			"full_description",
			"readers",
		]

	def get_readers(self, obj):
		return obj.readers.count()


class BookDeleteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		# fields = ['name']
