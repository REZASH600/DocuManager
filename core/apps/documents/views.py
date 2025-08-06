from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from apps.documents.models import DocumentCategory
from . import serializers, filters


class DocumentCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = serializers.DocumentCategorySerializer
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DocumentCategoryFilter




class DocumentCategoryUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "delete"]
    serializer_class = serializers.DocumentCategorySerializer
    queryset = DocumentCategory.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
