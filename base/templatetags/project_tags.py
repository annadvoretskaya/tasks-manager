from django import template

register = template.Library()


@register.filter(name='member_role')
def member_role(user, project):
    return user.role(project)


@register.filter
def is_owner(user, project):
    return project.is_owner(user)


@register.filter
def is_manager(user, project):
    return project.is_manager(user)


@register.filter
def is_developer(user, project):
    return project.is_developer(user)
