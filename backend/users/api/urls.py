from django.urls import re_path

from users.api import views


urlpatterns = [
    re_path(
        r"registration/", views.RegistrationView.as_view(), name="registration_view"
    ),
]
