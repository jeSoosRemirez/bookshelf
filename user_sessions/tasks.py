from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from users.models import User
from user_sessions.models import UserSession


@shared_task
def gather_user_session_info_task():
	seven_days_ago = timezone.now() - timedelta(days=7)
	old_sessions = UserSession.objects.all().filter(session_start__gte=seven_days_ago)

	for user_session in old_sessions:
		total_elapsed_time_by_book = {}

		if user_session.book and user_session.book.id:
			elapsed_time = user_session.get_elapsed_time()

			book_id = user_session.book.id
			total_elapsed_time_by_book[book_id] = (
				total_elapsed_time_by_book.get(book_id, timedelta()) + elapsed_time
			)

		user_profile, created = User.objects.get_or_create(id=user_session.user.id)
		user_profile.session_stats = {
			str(book_id): str(total_elapsed_time)
			for book_id, total_elapsed_time in total_elapsed_time_by_book.items()
		}
		user_profile.save()
