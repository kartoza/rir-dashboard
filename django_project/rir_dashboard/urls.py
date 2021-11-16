from django.conf.urls import url
from django.urls import include
from rir_dashboard.views.dashboard.admin.geography import (
    GeographyView, GeographyLevelManagementView, GeographyUploadView,
)
from rir_dashboard.views.dashboard.admin.indicator import (
    IndicatorValueManagementMapView, IndicatorCreateView,
    IndicatorManagementView, IndicatorEditView, IndicatorReportingUnitView
)
from rir_dashboard.views.dashboard.admin.instance import (
    InstanceManagementView, InstanceCreateView, InstanceEditView
)
from rir_dashboard.views.dashboard import (
    TrafficLightView, IndicatorView, IndicatorMapView
)

dashboard_url = [
    url(r'^indicator/(?P<pk>\d+)/value-manager', IndicatorValueManagementMapView.as_view(), name='indicator-value-mapview-manager'),
    url(r'^indicator/(?P<pk>\d+)', IndicatorMapView.as_view(), name='indicator-mapview'),
    url(r'^indicator', IndicatorView.as_view(), name='indicator-view'),
    url(r'^', TrafficLightView.as_view(), name='dashboard-view'),
]

admin_geography_url = [
    url(r'^upload', GeographyUploadView.as_view(), name='geography-upload-view'),
    url(r'^level-management', GeographyLevelManagementView.as_view(), name='geography-level-management-view'),
    url(r'^', GeographyView.as_view(), name='geography-management-view'),
]

admin_indicator_url = [
    url(r'^(?P<pk>\d+)/reporting-unit', IndicatorReportingUnitView.as_view(), name='indicator-reporting-unit'),
    url(r'^(?P<pk>\d+)/edit', IndicatorEditView.as_view(), name='indicator-edit'),
    url(r'^creat', IndicatorCreateView.as_view(), name='indicator-management-new'),
    url(r'^', IndicatorManagementView.as_view(), name='indicator-management-view'),
]
admin_instance_url = [
    url(r'^create', InstanceCreateView.as_view(), name='instance-management-create'),
    url(r'^edit', InstanceEditView.as_view(), name='instance-management-edit'),
    url(r'^', InstanceManagementView.as_view(), name='instance-management-view'),
]

admin_url = [
    url(r'^geography/', include(admin_geography_url)),
    url(r'^indicator/', include(admin_indicator_url)),
    url(r'^instance/', include(admin_instance_url)),
]

urlpatterns = [
    url(r'^dashboard/', include(dashboard_url)),
    url(r'^admin/', include(admin_url)),
]
