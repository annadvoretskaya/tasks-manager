from django import forms
from base.models import Task, Project, ApplicationUser


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')
        super(TaskForm, self).__init__(project, *args, **kwargs)
        self.fields['assigned_to'].queryset = project.list_members

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
