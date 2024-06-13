from django.urls import path, include
from rest_framework.routers import DefaultRouter
from korbo.auth.viewsets import (
    RegisterViewSet, LoginViewSet, RefreshTokenViewSet)

Router = DefaultRouter(trailing_slash=False)

Router.register(
    r"(?P<token_type>(consumer|consultant|startup))/auth", RegisterViewSet, 'register')
Router.register(
    r"(?P<token_type>(consumer|consultant|startup|admin|staff))/account", LoginViewSet, 'login')
# Router.register('auth/logout', LogoutViewSet, 'logout')
Router.register('auth/refresh', RefreshTokenViewSet, 'refresh')

urlpatterns = [
    path('', include(Router.urls))
]
