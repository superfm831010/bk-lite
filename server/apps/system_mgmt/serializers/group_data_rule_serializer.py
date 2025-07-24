from apps.core.utils.serializers import I18nSerializer
from apps.system_mgmt.models import GroupDataRule


class GroupDataRuleSerializer(I18nSerializer):
    class Meta:
        model = GroupDataRule
        fields = "__all__"
