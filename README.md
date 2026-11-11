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
- `/manage/` is the Nabd admin panel. Only Admin accounts can open it.

## Trainers

Trainers have a profile with a specialty and a bio. An admin assigns one
trainer to each member, and each trainer sees only their own members.

- `/trainers/` lists all trainers. Any logged-in user can open it.
- `/trainers/<id>/` shows a trainer's specialty and bio.
- `/trainers/me/edit/` lets a trainer create or edit their profile.
- `/trainers/me/members/` shows a trainer the members assigned to them.
- `/trainers/assign/` lets an admin assign a trainer to a member. Assigning a
  new trainer replaces the old one.

## Permissions

Use `role_required` to limit a view to certain roles. Users who are not logged
in are sent to the login page, and users with another role get a 403 page.

```python
from accounts.permissions import role_required

@role_required(User.Role.ADMIN, User.Role.TRAINER)
def my_view(request): ...
```

Import `User` from `accounts.models` as well.

## Notes for developers

- After pulling changes that touch the models, run `python manage.py migrate`.
- If migrate fails on an old local database, delete `db.sqlite3` and run it again.
- Pages extend `base.html`. Shared styles are in `accounts/static/css/site.css`.
- Run the tests with `python manage.py test`.
