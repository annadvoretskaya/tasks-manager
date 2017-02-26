from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from base.forms.invites import InviteForm
from base.forms.project import ProjectForm
from base.models import Project, Invite
from base.permissions import IsProjectOwnerPermission
from base.views.permissions import PermissionsMixin


class ProjectsByUserMixin(object):
    def get_queryset(self):
        queryset = super(ProjectsByUserMixin, self).get_queryset()
        return queryset.by_user(self.request.user)


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
    success_url = reverse_lazy('base:projects')
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





