from django.db import models
from users.models import User
from books.models import Book


class UserSession(models.Model):
	user = models.ForeignKey(
		User, related_name="user", on_delete=models.SET_NULL, null=True
	)
	book = models.ForeignKey(
		Book, related_name="book", on_delete=models.SET_NULL, null=True
	)
	session_start = models.DateTimeField(auto_now_add=True)
	session_end = models.DateTimeField(blank=True, null=True)

	def __init__(self, *args, **kwargs):
		super(UserSession, self).__init__(*args, **kwargs)
		self.session_start = self.session_start

	def save(self, *args, **kwargs):
		super(UserSession, self).save(*args, **kwargs)

	def get_elapsed_time(self):
		"""Calculates session duration for a record."""
		if self.session_end and self.session_start:
			return self.session_end - self.session_start
		return None
