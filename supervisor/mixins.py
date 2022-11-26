from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from core.utils import has_related_supervisor
class SupervisorMixin(AccessMixin):
    def dispatch(self , request, *args, **kwargs):
        if not request.user.is_authenticated or not has_related_supervisor(request.user):
            return redirect("login")
        return super().dispatch(request , *args ,**kwargs)