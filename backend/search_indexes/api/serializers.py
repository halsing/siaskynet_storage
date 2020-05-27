from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search_indexes.documents.storage import StorageDocument


class StorageDocumentSerializer(DocumentSerializer):
    class Meta:
        document = StorageDocument
        fields = (
            "name",
            "description",
            "category",
        )
