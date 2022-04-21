from django.shortcuts import redirect, reverse, render
from rir_dashboard.forms.instance import InstanceForm
from rir_dashboard.views.dashboard.admin._base import AdminView


class InstanceCreateView(AdminView):
    template_name = 'dashboard/admin/instance/form.html'

    @property
    def dashboard_title(self):
        return f'<span>Create New Instance</span>'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'form': InstanceForm(),
            'is_create': True
        }
        return context

    def post(self, request, **kwargs):
        form = InstanceForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            instance = form.save()
            return redirect(
                reverse(
                    'instance-management-view', args=[instance.slug]
                )
            )
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['is_create'] = True
        return render(
            request,
            self.template_name,
            context
        )
