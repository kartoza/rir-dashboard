from django.conf.urls import url
from django.urls import include
from rir_dashboard.views.dashboard.admin.geography import (
    GeographyView, GeographyLevelManagementView, GeographyUploadView,
)
from rir_dashboard.views.dashboard.admin.indicator import (
    IndicatorCreateView,
    IndicatorManagementView, IndicatorEditView, IndicatorReportingUnitView,
    IndicatorValueManagementMapView, IndicatorValueManagementTableView,
)
from rir_dashboard.views.dashboard.admin.instance import (
    InstanceManagementView, InstanceCreateView, InstanceEditView
)
from rir_dashboard.views.dashboard import (
    ContextAnalysisView, IndicatorView, indicator_detail_view
)
from rir_dashboard.views.dashboard.admin.harvesters import (
    HarvesterDetail
)
from rir_dashboard.views.dashboard.admin.harvesters.forms import (
    HarvesterAPIWithGeographyAndDateView, HarvestedUsingExposedAPIByExternalClientView
)

harvester_form_url = [
    url(r'^update/api-with-geography-and-date',
        HarvesterAPIWithGeographyAndDateView.as_view(),
        name=str(HarvesterAPIWithGeographyAndDateView.harvester_class).split("'")[1]
        ),
    url(
        r'^update/harvested-using-exposed-api-by-external-client',
        HarvestedUsingExposedAPIByExternalClientView.as_view(),
        name=str(HarvestedUsingExposedAPIByExternalClientView.harvester_class).split("'")[1]
    ),
]
dashboard_url = [
    url(r'^indicator/(?P<pk>\d+)/harvester/', include(harvester_form_url)),
    url(r'^indicator/(?P<pk>\d+)/harvester', HarvesterDetail.as_view(), name='harvester-detail'),
    url(r'^indicator/(?P<pk>\d+)/value-manager-map', IndicatorValueManagementMapView.as_view(), name='indicator-value-mapview-manager'),
    url(r'^indicator/(?P<pk>\d+)/value-manager-form', IndicatorValueManagementTableView.as_view(), name='indicator-value-form-manager'),
    url(r'^indicator/(?P<pk>\d+)', indicator_detail_view, name='indicator-detail'),
    url(r'^indicator', IndicatorView.as_view(), name='indicator-view'),
    url(r'^', ContextAnalysisView.as_view(), name='dashboard-view'),
]

admin_geography_url = [
    url(r'^upload', GeographyUploadView.as_view(), name='geography-upload-view'),
    url(r'^level-management', GeographyLevelManagementView.as_view(), name='geography-level-management-view'),
    url(r'^', GeographyView.as_view(), name='geography-management-view'),
]

admin_indicator_url = [
    url(r'^(?P<pk>\d+)/reporting-unit', IndicatorReportingUnitView.as_view(), name='indicator-reporting-unit'),
    url(r'^(?P<pk>\d+)/edit', IndicatorEditView.as_view(), name='indicator-edit'),
    url(r'^create', IndicatorCreateView.as_view(), name='indicator-management-new'),
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
