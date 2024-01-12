from rest_framework import serializers
from user_sessions.models import UserSession


class UserSessionDetailsSerializer(serializers.ModelSerializer):
	elapsed_time = serializers.DurationField(source="get_elapsed_time", read_only=True)

	class Meta:
		model = UserSession
		fields = ["id", "user", "book", "session_start", "session_end", "elapsed_time"]


class UserSessionListSerializerAPIView(serializers.ModelSerializer):
	elapsed_time = serializers.DurationField(source="get_elapsed_time", read_only=True)

	class Meta:
		model = UserSession
		fields = ["book", "session_start", "session_end", "elapsed_time"]


class UserSessionListAllSerializerAPIView(serializers.ModelSerializer):
	elapsed_time = serializers.DurationField(source="get_elapsed_time", read_only=True)

	class Meta:
		model = UserSession
		fields = ["id", "user", "book", "session_start", "session_end", "elapsed_time"]


class UserSessionCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSession
		fields = ["user", "book", "session_start", "session_end"]


class UserSessionDeleteSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSession
