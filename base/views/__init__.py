from .projects import ProjectsListView, ProjectDetailView, CreateProjectView, DeleteProjectView, UpdateProjectView, \
    JoinProjectView, RemoveMemberFromProjectView, ChangeRoleOnProjectView
from .tasks import CreateTaskView, TasksListView, DetailTaskView, UpdateTaskView, DeleteTaskView
from .users import SignUpView
from .invites import CreateInviteView

__all__ = ['ProjectsListView', 'ProjectDetailView', 'CreateTaskView', 'TasksListView', 'SignUpView',
           'CreateProjectView', 'DeleteProjectView', 'UpdateProjectView', 'CreateInviteView', 'JoinProjectView',
           'DetailTaskView', 'DeleteTaskView', 'RemoveMemberFromProjectView', 'ChangeRoleOnProjectView']

