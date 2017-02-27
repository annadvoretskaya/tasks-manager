from django.contrib import admin

# Register your models here.
from base.models import Project, Task, Invite, ApplicationUser


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
