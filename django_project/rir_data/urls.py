from django.conf.urls import url
from django.urls import include
from rir_data.api.indicator import IndicatorsList

api = [
    url(r'^indicator', IndicatorsList.as_view(), name='indicator_list'),
]

instance_url = [
    url(r'^api/', include(api)),
    url(r'^', include('rir_dashboard.urls')),
]

urlpatterns = [
    url(r'^(?P<slug>[^/]+)/', include(instance_url)),
]
