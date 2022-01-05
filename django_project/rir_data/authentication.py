from rest_framework import authentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rir_data.models import Instance


class IndicatorTokenAndBearerAuthentication(authentication.TokenAuthentication):
    keywords = ['Token', 'Bearer']

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() not in [keyword.lower().encode() for keyword in self.keywords]:
            msg = _('Token is required.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        kwargs = request.parser_context['kwargs']

        instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        indicator = get_object_or_404(
            instance.indicators, pk=kwargs.get('pk', 0)
        )
        if not indicator.api_exposed:
            msg = _('API is not exposed.')
            raise exceptions.AuthenticationFailed(msg)

        if str(indicator.api_token) != token:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)
        return None
