# coding=utf-8
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '13/10/21'

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from core.views.proxy import ProxyView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^proxy', ProxyView.as_view(), name='proxy-view'),
    url(r'^', include('rir_data.urls')),
]
