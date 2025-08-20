from rest_framework import serializers
from apps.log.models.log_group import LogGroup, LogGroupOrganization


class LogGroupSerializer(serializers.ModelSerializer):
    organizations = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="关联的组织ID列表"
    )

    class Meta:
        model = LogGroup
        fields = ["id", "name", "description", "rule", "created_by", "created_at", "organizations"]
        read_only_fields = ["created_by", "created_at"]

    def create(self, validated_data):
        organizations = validated_data.pop('organizations', [])
        log_group = super().create(validated_data)

        # 创建组织关联
        if organizations:
            LogGroupOrganization.objects.bulk_create(
                [LogGroupOrganization(log_group=log_group, organization=org_id)
                 for org_id in organizations],
                ignore_conflicts=True
            )

        return log_group

    def update(self, instance, validated_data):
        organizations = validated_data.pop('organizations', None)
        log_group = super().update(instance, validated_data)

        # 更新组织关联
        if organizations is not None:
            LogGroupOrganization.objects.filter(log_group=log_group).delete()
            LogGroupOrganization.objects.bulk_create(
                [LogGroupOrganization(log_group=log_group, organization=org_id)
                 for org_id in organizations],
                ignore_conflicts=True
            )

        return log_group
