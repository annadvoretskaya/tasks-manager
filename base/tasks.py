from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from mailing.shortcuts import render_send_email

from base.models import ApplicationUser, Task
from config.celery import app


@app.task()
def notify_user(user_id, task_ids):
    user = ApplicationUser.objects.get(id=user_id)
    tasks = Task.objects.filter(id__in=task_ids)

    if user.email:
        context = {'user': user, 'tasks': tasks}
        render_send_email([user.email], 'email/notification/deadline_notification', context)


@app.task()
def notify_users_about_deadline(user_ids):
    today = timezone.now().date()
    for user_id in user_ids:
        task_ids = list(Task.objects.filter(assigned_to_id=user_id, due_date=today).values_list('id', flat=True))
        notify_user.delay(user_id, task_ids)


@periodic_task(run_every=crontab(minute=0, hour='*/4'))
def check_users_deadlines():
    user_ids = list(ApplicationUser.objects.filter(tasks__isnull=False).values_list('id', flat=True).distinct())
    notify_users_about_deadline.delay(user_ids)
