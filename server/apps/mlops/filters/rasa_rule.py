from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_rule import RasaRule

class RasaRuleFilter(FilterSet):
    """
    Rasa机器人规则过滤器
    """
    class Meta:
        model = RasaRule
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }