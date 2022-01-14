from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rir_dashboard.views.dashboard._base import BaseDashboardView
from rir_data.models import Instance, Indicator


@login_required
def indicator_detail_view(request, slug, pk):
    if request.method == 'DELETE':
        instance = get_object_or_404(Instance, slug=slug)
        try:
            indicator = instance.indicators.get(
                id=pk
            )
            indicator.delete()
            return HttpResponse('OK')
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')
