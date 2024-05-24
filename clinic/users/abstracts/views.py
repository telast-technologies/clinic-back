from typing import Any

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BaseProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Any:
        raise NotImplementedError

    def invalidate_prefetch_cache(self, instance):
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}


class ProfileGetViewSet(BaseProfileViewSet):
    @action(detail=False, methods=["GET"], url_path="details")
    def get_profile(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def invalidate_prefetch_cache(self, instance):
        super().invalidate_prefetch_cache(instance)


class ProfileUpdateViewSet(BaseProfileViewSet):
    @action(detail=False, methods=["PATCH"], url_path="update")
    def update_profile(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.invalidate_prefetch_cache(instance)

        return Response(serializer.data)

    def invalidate_prefetch_cache(self, instance):
        super().invalidate_prefetch_cache(instance)


class ProfileViewSet(ProfileGetViewSet, ProfileUpdateViewSet):
    def invalidate_prefetch_cache(self, instance):
        super().invalidate_prefetch_cache(instance)


class PasswordResetConfirmRedirect(views.APIView):
    permission_classes = []
    serializer_class = None

    def get(self, request, uidb64, token, *args, **kwargs):
        return HttpResponseRedirect(f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}/{uidb64}/{token}/")
