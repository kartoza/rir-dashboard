from django.conf.urls import url
from django.urls import include
from rir_dashboard.views.dashboard.admin import (
    GeographyView, LevelManagementView
)
from rir_dashboard.views.dashboard import (
    TrafficLightView, IndicatorView, IndicatorMapView
)

dashboard_url = [
    url(r'^indicator/(?P<pk>\d+)', IndicatorMapView.as_view(), name='indicator-mapview'),
    url(r'^indicator', IndicatorView.as_view(), name='indicator-view'),
    url(r'^', TrafficLightView.as_view(), name='dashboard-view'),
]

admin_geography_url = [
    url(r'^level-management', LevelManagementView.as_view(), name='level-management-view'),
    url(r'^', GeographyView.as_view(), name='geography-management-view'),
]

admin_url = [
    url(r'^geography/', include(admin_geography_url)),
]

urlpatterns = [
    url(r'^dashboard/', include(dashboard_url)),
    url(r'^admin/', include(admin_url)),
]
