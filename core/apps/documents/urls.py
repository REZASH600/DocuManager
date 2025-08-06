from django.urls import path
from .views import (
    DocumentCategoryListCreateAPIView,
    DocumentCategoryUpdateDestroyAPIView,
    DocumentCreateAPIView,
)


app_name = "documents"
urlpatterns = [
    path(
        "categories/",
        DocumentCategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:pk>/",
        DocumentCategoryUpdateDestroyAPIView.as_view(),
        name="category-update-delete",
    ),
    path("", DocumentCreateAPIView.as_view(), name="document-create"),
]
