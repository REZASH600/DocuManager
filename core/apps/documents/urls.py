from django.urls import path
from .views import (
    DocumentCategoryListCreateAPIView,
    DocumentCategoryUpdateDestroyAPIView
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

]
