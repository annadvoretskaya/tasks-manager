from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.base import View

from base.forms import InviteForm, ProjectForm
from base.mixins import ProjectsByUserMixin, PermissionsMixin
from base.models import Project, Invite, ApplicationUser
from base.permissions import IsProjectOwnerPermission


class ProjectsListView(LoginRequiredMixin, ProjectsByUserMixin, ListView):
    template_name = 'project/project_list.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(LoginRequiredMixin, ProjectsByUserMixin, DetailView):
    model = Project
    context_object_name = 'projects'
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['invite_form'] = InviteForm()
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateProjectView(CreateView):
    model = Project
    fields = ['title', 'description']
    template_name = 'project/project_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.object.managers.add(self.request.user)
        return super(CreateProjectView, self).form_valid(form)


class UpdateProjectView(ProjectsByUserMixin, PermissionsMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'
    permission_classes = [IsProjectOwnerPermission]


class DeleteProjectView(ProjectsByUserMixin, PermissionsMixin, DeleteView):
    model = Project
    template_name = 'project/project_confirm_delete.html'
    success_url = reverse_lazy('base:projects-list')
    permission_classes = [IsProjectOwnerPermission]


class JoinProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project/project_join.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        return super(JoinProjectView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Invite, pk=self.pk)

    def get_context_data(self, **kwargs):
        context = super(JoinProjectView, self).get_context_data(**kwargs)
        context['project'] = self.get_object().project

        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object().project
        project.developers.add(request.user)

        return redirect(reverse('base:project-detail', args=(project.pk, )))


class RemoveMemberFromProjectView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        project_pk = kwargs.get('project_pk')
        member_pk = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        member = get_object_or_404(ApplicationUser, pk=member_pk)
        project.remove_member(member)

        return redirect(reverse('base:project-detail', args=(project_pk,)))


class ChangeRoleOnProjectView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        project_pk = kwargs.get('project_pk')
        member_pk = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        member = get_object_or_404(ApplicationUser, pk=member_pk)
        project.swap_roles(member)
        return redirect(reverse('base:project-detail', args=(project_pk,)))


__all__ = ['ProjectsListView', 'ProjectDetailView', 'CreateProjectView', 'DeleteProjectView',
           'UpdateProjectView', 'JoinProjectView', 'RemoveMemberFromProjectView', 'ChangeRoleOnProjectView']
