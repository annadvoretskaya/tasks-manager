from django import forms

from base.models import Project


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        project = kwargs.get('instance', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['managers'].queryset = project.list_members.exclude(pk=project.owner.pk)
        self.fields['developers'].queryset = project.list_members

    class Meta:
        model = Project
        fields = ['title', 'description', 'managers', 'developers']
