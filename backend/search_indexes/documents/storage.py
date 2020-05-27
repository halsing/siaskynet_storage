from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer

from skynet_storage import settings
from storage import models as storage_models

STORAGE_INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
STORAGE_INDEX.settings(
    number_of_shards=1, number_of_replicas=0,
)

html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"],
)


@STORAGE_INDEX.doc_type
class StorageDocument(Document):
    """Storage elasticsearch document"""

    name = StringField(
        analyzer=html_strip, fields={"raw": StringField(analyzer="keyword")}
    )
    description = StringField(
        analyzer=html_strip, fields={"raw": StringField(analyzer="keyword")}
    )
    category = fields.ObjectField(
        properties={
            "name": StringField(
                analyzer=html_strip,
                fields={"raw": KeywordField(), "suggest": fields.CompletionField()},
            )
        }
    )

    class Django:
        """Inner nested class Django."""

        model = storage_models.File
