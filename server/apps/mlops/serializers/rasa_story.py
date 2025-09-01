from rest_framework import serializers
from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_story import RasaStory

class RasaStorySerializer(AuthSerializer):
    permission_key = "dataset.rasa_story"

    slot_count = serializers.SerializerMethodField(read_only=True, help_text="槽位数量")
    form_count = serializers.SerializerMethodField(read_only=True, help_text="表单数量")
    intent_count = serializers.SerializerMethodField(read_only=True, help_text="意图数量")
    response_count = serializers.SerializerMethodField(read_only=True, help_text="响应数量")

    class Meta:
        model = RasaStory
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'steps': {'required': False},
            'dataset': {'required': False},
        }

    def get_intent_count(self, obj):
        return self._count_steps_by_type(obj.steps, 'intent')

    def get_slot_count(self, obj):
        return self._count_steps_by_type(obj.steps, 'slot')

    def get_form_count(self, obj):
        return self._count_steps_by_type(obj.steps, 'form')

    def get_response_count(self, obj):
        return self._count_steps_by_type(obj.steps, 'response')

    def _count_steps_by_type(self, steps, step_type):
        """
        统计 steps 中 type 为指定类型的数量
        """
        if not steps:
            return 0
        return sum(1 for step in steps if isinstance(step, dict) and step.get('type') == step_type)
