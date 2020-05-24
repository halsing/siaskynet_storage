from django.shortcuts import get_object_or_404, redirect, reverse
from rest_framework import (
    authentication,
    viewsets,
    permissions,
    parsers,
    renderers,
    status,
    mixins,
)
from rest_framework.response import Response
from rest_framework.decorators import action

from siaskynet import Skynet

from storage.models import File
from storage.api.serializers import FileSerializer
from storage.api.permissions import IsOwner


class FileView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    parser_classes = [parsers.MultiPartParser]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    serializer_class = FileSerializer

    def get_permissions(self):
        if self.action in ["list", "create"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return File.objects.filter(owner=user)
        else:
            self.permission_denied(self.request)

    def perform_create(self, serializer):
        temp_file = self.request.data["file"]
        skylink = Skynet.UploadFile(temp_file)
        serializer.save(file=skylink, owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsOwner])
    def change_public(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)
        file.public = not file.public
        file.save()

        url = reverse("file-detail", args=[pk])
        return redirect(url)


class PublicFileView(viewsets.ReadOnlyModelViewSet):
    parser_classes = [parsers.JSONParser]
    permission_classes = [permissions.AllowAny]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter(public=True)
