from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
	"""
	User registration serializer and creating a new one.
	"""

	password = serializers.CharField(max_length=128, min_length=8, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	class Meta:
		model = User
		fields = ["id", "email", "username", "password", "token"]

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	username = serializers.CharField(max_length=255, read_only=True)
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		email = data.get("email", None)
		password = data.get("password", None)

		if not email:
			raise serializers.ValidationError("An email address is required to log in.")

		if not password:
			raise serializers.ValidationError("A password is required to log in.")

		user = authenticate(username=email, password=password)

		if not user:
			raise serializers.ValidationError(
				"A user with this email and password was not found."
			)

		if not user.is_active:
			raise serializers.ValidationError("This user has been deactivated.")

		return {"email": user.email, "username": user.username, "token": user.token}


class UserSerializer(serializers.ModelSerializer):
	"""Ощуществляет сериализацию и десериализацию объектов User."""

	password = serializers.CharField(max_length=128, min_length=8, write_only=True)

	class Meta:
		model = User
		fields = ("email", "username", "password", "session_stats")

	def update(self, instance, validated_data):
		"""Выполняет обновление User."""
		password = validated_data.pop("password", None)

		for key, value in validated_data.items():
			setattr(instance, key, value)

		if password:
			instance.set_password(password)

		instance.save()

		return instance
