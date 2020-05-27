from rest_framework.routers import SimpleRouter

from search_indexes.api import views


router = SimpleRouter()

router.register(
    prefix=r"search", viewset=views.StorageDocumentView, basename="file_search"
)

urlpatterns = router.urls
