from rest_framework import serializers

from storage.models import File
from storage.validators import validate_link


class FileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    siasky_link = serializers.CharField(source="generate_link", read_only=True)

    class Meta:
        model = File
        fields = (
            "url",
            "id",
            "name",
            "file",
            "owner",
            "public",
            "created",
            "updated",
            "siasky_link",
        )
