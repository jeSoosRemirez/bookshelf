from django.db import models
from users.models import User


class Book(models.Model):
	author = models.TextField(db_index=True, blank=False)
	name = models.TextField(blank=False)
	publish_year = models.IntegerField(db_index=True, blank=True, default=1984)
	full_description = models.TextField(blank=True)
	short_description = models.TextField(blank=True)
	readers = models.ManyToManyField(User, related_name="readers")
	created_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["created_time"]

	def __init__(self, *args, **kwargs):
		super(Book, self).__init__(*args, **kwargs)
		self.created_time = self.created_time

	def save(self, *args, **kwargs):
		super(Book, self).save(*args, **kwargs)
