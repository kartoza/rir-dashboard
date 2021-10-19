from django.conf.urls import url
from rir_dashboard.views.dashboard import DashboardView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard_view'),
]
