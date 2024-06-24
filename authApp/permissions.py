from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def check_role(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and user.role.name in allowed_roles:
                return view_func(self, request, *args, **kwargs)
            else:
                return Response({"error": "Acceso denegado. Permisos insuficientes."},
                                status=status.HTTP_401_UNAUTHORIZED)
        return _wrapped_view
    return decorator
