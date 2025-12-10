from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """Protect selected endpoints by requiring a session user."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_prefixes = ['/add', '/edit', '/delete', '/blogs']

    def __call__(self, request):
        path = request.path
        if self._needs_auth(path) and not request.session.get('user_id'):
            login_url = reverse('login')
            return redirect(f"{login_url}?next={path}")
        return self.get_response(request)

    def _needs_auth(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self.protected_prefixes)
