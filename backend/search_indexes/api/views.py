from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from search_indexes.api.serializers import StorageDocumentSerializer
from search_indexes.documents.storage import StorageDocument


class StorageDocumentView(DocumentViewSet):
    """The StorageDocument view based on Elasticsearch"""

    document = StorageDocument
    serializer_class = StorageDocumentSerializer
    lookup_field = "name"
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        "name",
        "description",
        "category.name",
    )

    filter_fields = {
        "category": {
            "field": "category.name.raw",
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
    }

    ordering_fields = {
        "name": "name.raw",
        "category": "category.name.raw",
    }

    # Default ordering
    ordering = ("name",)
