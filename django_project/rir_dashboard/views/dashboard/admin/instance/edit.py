from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.forms.instance import InstanceForm
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Instance


class InstanceEditView(AdminView):
    template_name = 'dashboard/admin/instance/form.html'

    @property
    def dashboard_title(self):
        return f'<span>Edit Instance</span>'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        context = {
            'form': InstanceForm(
                initial=InstanceForm.model_to_initial(self.instance)
            )
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )

        form = InstanceForm(
            request.POST,
            request.FILES,
            instance=self.instance
        )
        if form.is_valid():
            instance = form.save()
            if request.POST.get('icon_delete', None):
                instance.icon = None
                instance.save()
            return redirect(
                reverse(
                    'instance-management-view', args=[self.instance.slug]
                )
            )
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(
            request,
            self.template_name,
            context
        )
