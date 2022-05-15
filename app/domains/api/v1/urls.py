from django.urls import path
from domains.api.v1 import views

urlpatterns = [
    path("domains", views.DomainsListApi.as_view()),
]
