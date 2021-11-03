from abc import ABC
from braces.views import SuperuserRequiredMixin
from rir_dashboard.views.dashboard._base import BaseDashboardView


class AdminView(ABC, SuperuserRequiredMixin, BaseDashboardView):
    pass
