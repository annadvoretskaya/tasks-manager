# Trello like project

App consists of next models: ApplicationUser, Project, Task, Invite. 
User can register in the app by himself, create projects and tasks and invite new users to the project. 
Invited user can join the project (by the link from email) after login (or registration if there are not such user in the app).
Project has next user roles: owner, managers, developers, owner of project is manager by default.
Owner can invite users, update and delete project, remove members from project and change their role, create, update and delete tasks.
Manager can invite users, create, update and delete tasks.

# Project initialization
## 1. Create virtual environment

1. Clone repository: ``git clone https://github.com/annadvoretskaya/test_project.git``
2. Create virtual environment: ``mkvirtualenv test_project``
3. Install requirements ``pip install -r requirements.txt``
```
workon test_project
```

## 2. Database
1. Migrations: ``./manage.py migrate``

## 3. Run project
1. ``./manage.py runserver``

## 4. Run celery
1. ``celery worker -A config``
2. ``celery beat -A config``
