from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
	PermissionsMixin,
	BaseUserManager,
)


class UserManager(BaseUserManager):
	"""
	Custom user manager.
	"""

	def create_user(self, username, email, password=None):
		"""
		Creates a regular user.

		Args:
		    username (_type_): username
		    email (_type_): email
		    password (_type_, optional): password. Defaults to None.

		Raises:
		    TypeError: if 'username' or 'email' were not provided.

		Returns:
		    user: User type.
		"""
		if not username:
			raise TypeError("User must have a username.")
		if not email:
			raise TypeError("User must have an email address.")

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save()

		return user

	def create_superuser(self, username, email, password):
		"""
		Creates a superuser.

		Args:
		    username (_type_): username
		    email (_type_): email
		    password (_type_): password

		Raises:
		    TypeError: if password was not provided.

		Returns:
		    user: User type.
		"""
		if not password:
			raise TypeError("Superusers must have a password.")

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""
	User base model.
	"""

	username = models.CharField(db_index=True, max_length=255, unique=True)
	email = models.EmailField(db_index=True, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	token_key = models.CharField(max_length=512, default="")
	session_stats = models.JSONField(default=dict)

	# Fields for login
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	objects = UserManager()
