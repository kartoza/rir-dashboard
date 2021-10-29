from django.conf.urls import url
from django.urls import include
from rir_dashboard.views.dashboard import (
    DashboardHomeView, IndicatorView, IndicatorMapView
)
from rir_dashboard.views.traffic_light import TrafficLightView

dashboard_url = [
    url(r'^indicator/(?P<pk>\d+)', IndicatorMapView.as_view(), name='indicator-mapview'),
    url(r'^indicator', IndicatorView.as_view(), name='indicator-view'),
    url(r'^', DashboardHomeView.as_view(), name='dashboard-view'),
]
urlpatterns = [
    url(r'^dashboard/', include(dashboard_url)),
    url(r'^$', TrafficLightView.as_view(), name='traffic-light-view'),
]
