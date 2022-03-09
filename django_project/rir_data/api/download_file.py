import mimetypes
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from core.permissions import AdminAuthenticationPermission
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound


class DownloadSharepointFile(APIView):
    """
    Download sharepoint file
    """
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def get(self, request, slug):
        filepath = request.GET.get('file', None)
        if not filepath:
            return HttpResponseBadRequest('file is required in parameter')
        try:
            if not os.path.exists(filepath):
                return HttpResponseNotFound(f'{filepath} is not found')

            fl = open(filepath, 'rb')
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filepath)
            return response
        except UnicodeEncodeError:
            return HttpResponseBadRequest('file need to be encoded')
