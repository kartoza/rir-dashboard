from django.contrib.auth.views import LoginView


class DashboardView(LoginView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
