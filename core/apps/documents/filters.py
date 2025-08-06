import django_filters
from apps.documents.models import DocumentCategory


class DocumentCategoryFilter(django_filters.FilterSet):
    only_active_type = django_filters.BooleanFilter(method="filter_only_active_type")

    class Meta:
        model = DocumentCategory
        fields = ["participant_id", "id"]

    def filter_only_active_type(self, queryset, name, value):
        if value:
            return queryset.filter(document_types__is_active=True).distinct()
        return queryset