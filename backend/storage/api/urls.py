from django.urls import path, include
from rest_framework.routers import DefaultRouter

from storage.api import views

router = DefaultRouter()
router.register(r"priv-files", views.FileView, basename="file")
router.register(r"public-files", views.PublicFileView, basename="public")

urlpatterns = router.urls
