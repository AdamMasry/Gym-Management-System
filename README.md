# Nabd

Nabd is a gym management system built with Django. Members sign up and log in,
and each account has a role: Admin, Trainer or Member.

## Run locally

1. Clone the repo and go into the folder.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install the packages: `pip install -r requirements.txt`
5. Create the database: `python manage.py migrate`
6. Create an admin account: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`
8. Open http://127.0.0.1:8000

## Pages

- `/signup/` creates an account. New accounts start as Member.
- `/login/` logs in with email and password.
- `/admin/` is the admin panel for staff accounts.

## Notes for developers

- After pulling changes that touch the models, run `python manage.py migrate`.
- If migrate fails on an old local database, delete `db.sqlite3` and run it again.
- Pages extend `base.html`. Shared styles are in `accounts/static/css/site.css`.
