from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from base.forms import TaskForm
from base.mixins import ProjectTasksMixin, PermissionsMixin
from base.models import Task, Project
from base.permissions import IsTaskOwnerOrManagerPermission


class TasksListView(LoginRequiredMixin, ProjectTasksMixin, ListView):
    template_name = 'tasks.html'
    model = Task
    context_object_name = 'tasks'


class CreateTaskView(LoginRequiredMixin, PermissionsMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    permission_classes = [IsTaskOwnerOrManagerPermission, ]

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk', None)
        self.object = form.save(commit=False)
        self.object.project_id = project_id
        self.object.save()

        return super(CreateTaskView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk', None))
        kwargs['project'] = project
        return kwargs


class DetailTaskView(LoginRequiredMixin, ProjectTasksMixin, DetailView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_detail.html'


class UpdateTaskView(LoginRequiredMixin, ProjectTasksMixin, PermissionsMixin, UpdateView):
    model = Task
    permission_classes = [IsTaskOwnerOrManagerPermission, ]
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super(UpdateTaskView, self).get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk', None))
        kwargs['project'] = project
        return kwargs


class DeleteTaskView(LoginRequiredMixin, ProjectTasksMixin, PermissionsMixin, DeleteView):
    model = Task
    permission_classes = [IsTaskOwnerOrManagerPermission, ]

    def get_success_url(self):
        return reverse('base:project-detail', args=self.kwargs.get('project_pk'))


__all__ = ['TasksListView', 'CreateTaskView', 'DetailTaskView', 'UpdateTaskView', 'DeleteTaskView']
