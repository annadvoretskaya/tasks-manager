from django import forms

from base.models import Task


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = project.list_members

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': DateInput()
        }
