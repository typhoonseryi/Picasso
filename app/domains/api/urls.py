from django.urls import include, path

urlpatterns = [
    path("v1/", include("domains.api.v1.urls")),
]
