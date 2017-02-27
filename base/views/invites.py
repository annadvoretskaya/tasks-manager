from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from base.forms import InviteForm
from base.mixins import PermissionsMixin
from base.permissions import IsProjectOwnerOrManagerPermission


class CreateInviteView(PermissionsMixin, View):
    http_method_names = ['post']
    permission_classes = [IsProjectOwnerOrManagerPermission, ]

    def post(self, request, *args, **kwargs):
        form = InviteForm(request.POST)
        project_id = kwargs.get('pk')
        if form.is_valid():
            invite = form.save(commit=False)
            invite.project_id = project_id
            invite.save()
            invite.send()
        messages.success(request, "Ok! Send.")
        return redirect(reverse('base:project-detail', args=(project_id, )))


__all__ = ['CreateInviteView', ]
