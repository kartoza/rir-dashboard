from django.conf.urls import url
from rir_dashboard.views.traffic_light import TrafficLightView

urlpatterns = [
    url(r'^$', TrafficLightView.as_view(), name='traffic_light_view'),
]
