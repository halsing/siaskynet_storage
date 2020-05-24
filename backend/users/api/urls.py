from django.urls import path, re_path, include

from users.api import views


urlpatterns = [
    re_path(
        r"registration/", views.RegistrationView.as_view(), name="registration_view"
    ),
]
