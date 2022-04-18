from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import AdminAuthenticationPermission
from rir_data.models.instance import Instance
from rir_data.models.indicator import Indicator


class IndicatorShow(APIView):
    """
    Change indicator show
    """
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def post(self, request, slug, pk):
        """
        Save reporting units of indicator

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            indicator = instance.indicators.get(id=pk)
            indicator.show_in_context_analysis = True
            indicator.save()
            return Response('OK')
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')


class IndicatorHide(APIView):
    """
    Change indicator show
    """
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def post(self, request, slug, pk):
        """
        Save reporting units of indicator

        :param slug: slug of the instance
        :param pk: pk of the indicator
        :return:
        """
        try:
            instance = get_object_or_404(
                Instance, slug=slug
            )
            indicator = instance.indicators.get(id=pk)
            indicator.show_in_context_analysis = False
            indicator.save()
            return Response('OK')
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')
