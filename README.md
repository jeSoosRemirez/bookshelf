
# Before the start:

**Create/Enter poetry env**

	If no poetry env was created before
	`$ poetry init`

	To enter poetry env
	`$ poetry shell`

**Install dependencies**

	`$ poetry install`

**Make migrations**

	`$ python manage.py makemigrations`
	`$ python manage.py migrate`

**Load fixtures(if necessary)**

	Fixtures are stored inside `application_name/fixtures/app_fixtures.json`
	To load fixtures
	`$ python manage.py loaddata path/to/fixtures.json`

	**Fixtures paths:**
		users -> `users/fixtures/users_fixtures.json`
		books -> `books/fixtures/books_fixtures.json`
		users -> `user_sessions/fixtures/user_sessions_fixtures.json`

**Base users from fixtures and their credentials**

	Admin:
		username: admin
		email: admin@mail.com
		password: admin1234

	Test user
			username: test1
			email: test1@mail.com
			password: test1234

### How to run server:
`$ python manage.py runserver`

### How to run tests:
`$ python manage.py test path/to/tests/dir`

### How to run celery task
Before runing the task redis should be running.
`$ docker-compose up -d`

In django admin add periodic task. Give task a name then in `Task (registered)` choose `user_sessions.tasks.gather_user_session_info_task`.  In `crontab` schedule
press plus button and without changing anything save it, then choose what you have created.
Save the task in the bottom of the page. Select the task that you have created, in `Action` field choose `Run selected tasks` and press button `Go`. 

The collected data you should observe at `/users/` endpoint.
If there is no data run `$ celery -A bookshelf worker -l info` and run the task again.

## some info
🔐 - the Bearer token should be provided

🔓 - available to everyone

👤 - access only for admin users(and Bearer token)

# Endpoints:

## Users

🔓 **/users/register/**

(POST) create a user.

	Body:
	{
		"username": str,
		"email": str,
		"password": str(>=8)
	}
	Response:
		{"email": str, "username": str}

🔓 **/users/login/**

(POST) login user to retrieve access_token and refresh_token.

	Body:
		{"email": str, "password": str}
	Response:
		{"refresh": refresh_token, "access": access_token}

🔐 **/users/login/refresh/**

(POST) retrieve new refresh_token.

	Body:
		{"refresh": refresh_token}
	Response:
		{"access": new_access_token}

🔐 **/users/**

(GET) retrieve user details.

	Response:
		dict: {"email": str, "username": str, "session_stats": dict}

🔐 **/users/**

(PATCH) update user data.

	Body:
		{"email: "new_email", "username": "new_username"}.
	Response:
		dict: {"email": str, "username": str, "session_stats": dict}


## Books

🔐 **/books/**

(GET) retrieve all books.

	Response:
	{
		"id": id,
		"author": str,
		"name": str,
		"publish_year": int,
		"short_description": str,
		"readers": int
	}, ...

👤 **/books/<int:pk>/**

(GET) retrieve a book detailed info, pk is required.

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

👤 **/books/delete/<int:pk>/**

(DELETE) delete a book by id.


## User Sessions

🔐 **/books/sessions/detailed/**

🔐 **/books/<int:pk>/sessions/detailed/**

(GET) If pk, retrieve data for a book; if not pk, retrieve data for all books.

	Response:
	{
		"id": id,
		"user": pk,
		"book": pk,
		"sessions_start": datetime,
		"session_end": datetime,
		"elapsed_time": datetime
	}

🔐 **/books/sessions/**

🔐 **/books/<int:pk>/sessions/**

(GET) If pk, retrieve time for a book; if not pk, retrieve time for all books.

	Response:
	{
		"book": pk,
		"total_elapsed_time": datetime
	}

🔐 **/books/<int:pk>/sessions/start_end/**  

(POST) start a session with a book;

(PATCH) end a session with a book. The session going to auto-end
if another session has started and a previous one was not ended.

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

👤 **/books/sessions/create/**

(POST) create a session record. 

	Body:
	{
		"user": pk,
		"book": pk,
		"session_start": datetime,
		"session_end": datetime
	}

👤 **/books/sessions/<int:pk>/**

(GET) retrieve a session record, pk should be provided in url.

	Response:
	{
		"id": pk,
		"user": pk,
		"book": pk,
		"session_start": datetime,
		"session_end": datetime,
		"elapsed_time": datetime
	}

👤 **/books/sessions/all/**

(GET) retrieve all session records.

	Response:
	{
		"id": pk,
		"user": pk,
		"book": pk,
		"session_start": datetime,
		"session_end": datetime,
		"elapsed_time": datetime
	}, ...

👤 **/books/sessions/delete/<int:pk>/**

(DELETE) delete a session record, pk should be provided in url.
