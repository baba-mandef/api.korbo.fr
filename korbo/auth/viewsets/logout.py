from django.contrib.auth import user_logged_out
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from korbo.auth.serializers import LogoutSerializer
from korbo.extra.tools import validate_jwt


class LogoutViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def get_token_id(self):
        token_jwt = get_authorization_header(self.request).split()[1].decode()
        payload = validate_jwt(token_jwt)
        if not payload:
            raise AuthenticationFailed()
        return payload["token"]

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            getattr(user, f"{self.request.auth}_token_set").filter(public_id=self.get_token_id()).delete()
        except AttributeError:
            raise AuthenticationFailed()

        user_logged_out.send(sender=user.__class__, request=request, user=user)
        request.session.flush()

        return Response({"detail": True}, status=status.HTTP_200_OK)
