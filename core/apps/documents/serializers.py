from rest_framework import serializers
from apps.documents.models import DocumentCategory, DocumentType, Document
from django.db.models import Count, Q, Sum


class DocumentTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DocumentType
        fields = [
            "id",
            "title",
            "private_visible",
            "public_visible",
            "is_active",
        ]


class DocumentCategorySerializer(serializers.ModelSerializer):
    types = serializers.SerializerMethodField()
    document_types_input = DocumentTypeSerializer(
        many=True, write_only=True, required=False
    )

    document_count = serializers.SerializerMethodField()

    class Meta:
        model = DocumentCategory
        fields = [
            "id",
            "title",
            "participant",
            "company_id",
            "types",
            "document_types_input",
            "document_count",
        ]

    def get_types(self, obj):
        # Only return active document types
        active_types = obj.document_types.filter(is_active=True, is_deleted=False)
        return DocumentTypeSerializer(active_types, many=True).data

    def get_document_count(self, obj):
        return (
            obj.document_types.annotate(
                active_doc_count=Count(
                    "documents",
                    filter=Q(documents__is_active=True, documents__is_deleted=False),
                )
            ).aggregate(total=Sum("active_doc_count"))["total"]
            or 0
        )

    def create(self, validated_data):
        types_data = validated_data.pop("document_types_input", [])
        category = DocumentCategory.objects.create(**validated_data)
        for type_data in types_data:
            DocumentType.objects.create(category=category, **type_data)
        return category

    def update(self, instance, validated_data):
        types_data = validated_data.pop("document_types_input", None)
        instance = super().update(instance, validated_data)

        if types_data is not None:
            for type_data in types_data:
                type_id = type_data.get("id")
                if type_id:
                    try:
                        doc_type = DocumentType.objects.get(
                            id=type_id, category=instance
                        )
                        for attr, value in type_data.items():
                            setattr(doc_type, attr, value)
                        doc_type.save()
                    except DocumentType.DoesNotExist as e:
                        raise serializers.ValidationError(
                            f"DocumentType with id {type_id} does not exist in this category."
                        )
                else:
                    DocumentType.objects.create(category=instance, **type_data)

        return instance


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "company_id",
            "participant",
            "document_type",
            "file",
            "is_active",
        ]
