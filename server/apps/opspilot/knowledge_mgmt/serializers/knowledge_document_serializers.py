from rest_framework import serializers

from apps.opspilot.models import KnowledgeDocument
from config.drf.serializers import UsernameSerializer


class KnowledgeDocumentSerializer(UsernameSerializer):
    train_status_display = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeDocument
        fields = "__all__"

    @staticmethod
    def get_train_status_display(obj):
        return obj.get_train_status_display()
