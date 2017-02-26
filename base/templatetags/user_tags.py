from django import template

register = template.Library()


@register.filter(name='member_role')
def member_role(user, project):
    return user.role(project)
