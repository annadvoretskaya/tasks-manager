from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mailing.shortcuts import render_send_email

from config import settings


class ProjectQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(Q(owner=user) | Q(managers=user) | Q(developers=user)).distinct()


class ApplicationUser(AbstractUser):
    email = models.EmailField(_('Email address'))

    def __unicode__(self):
        return "User: {0}".format(self.username)


class Project(models.Model):
    title = models.CharField(_('Title'), max_length=256)
    description = models.TextField(_('Description'), blank=True)
    owner = models.ForeignKey(ApplicationUser, verbose_name=_('Owner'), related_name='owner_projects')
    managers = models.ManyToManyField(ApplicationUser, verbose_name=_('Managers'), related_name='managers_projects', blank=True)
    developers = models.ManyToManyField(ApplicationUser, verbose_name=_('Developers'),
                                        related_name='developer_projects', blank=True)

    objects = ProjectQuerySet.as_manager()

    OWNER = 'owner'
    MANAGER = 'manager'
    DEVELOPER = 'developer'

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return "Project: {0}".format(self.title)

    def is_owner(self, user):
        return user == self.owner

    def is_manager(self, user):
        return self.is_owner(user) or self.managers.filter(pk=user.pk).exists()

    def is_developer(self, user):
        return self.developers.filter(pk=user.pk).exists()

    def get_absolute_url(self):
        return reverse('base:project-detail', args=(self.pk, ))

    @property
    def list_members(self):
        return self.managers.all() | self.developers.all()

    def remove_member(self, user):
        if self.is_manager(user):
            self.managers.remove(user)
        else:
            self.developers.remove(user)

    def swap_roles(self, user):
        if self.is_manager(user):
            self.managers.remove(user)
            self.developers.add(user)
        else:
            self.developers.remove(user)
            self.managers.add(user)

    def role_on_project(self, user):
        if self.is_owner(user):
            return self.OWNER
        elif self.is_manager(user):
            return self.MANAGER
        return self.DEVELOPER


class Task(models.Model):
    title = models.CharField(_('Title'), max_length=256)
    description = models.TextField(_('Description'), blank=True)
    due_date = models.DateTimeField(_('Due date'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='tasks')
    assigned_to = models.ForeignKey(ApplicationUser, verbose_name=_('Assigned to'),
                                    related_name='tasks', null=True, blank=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __unicode__(self):
        return "Task: {0}".format(self.title)

    def get_absolute_url(self):
        return reverse('base:task-detail', args=(self.project_id, self.pk))


def get_uuid():
    return str(uuid.uuid4())


class Invite(models.Model):
    """Model for inviting users to the project"""

    uuid = models.UUIDField(primary_key=True, default=get_uuid)
    email = models.EmailField()
    project = models.ForeignKey(Project, null=True)

    def __unicode__(self):
        return str(self.uuid)

    def _get_invite_url(self):
        return "{}{}".format(settings.BASE_URL, reverse('base:project-join', args=(self.pk, )))

    def send(self):
        context = {'url': self._get_invite_url()}
        render_send_email([self.email, ], 'email/invite/invite', context)
