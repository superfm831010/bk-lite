import os
from apps.mlops.models.rasa_intent import RasaIntent
from apps.mlops.models.rasa_rule import RasaRule
from apps.mlops.models.rasa_story import RasaStory
from apps.mlops.models.rasa_slot import RasaSlot
from apps.mlops.models.rasa_response import RasaResponse
from apps.mlops.models.rasa_entity import RasaEntity
from apps.mlops.models.rasa_form import RasaForm

class RasaYamlExporter:
    def __init__(self,dataset_id):
        self.dataset_id = dataset_id
        self.intents = RasaIntent.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.rules = RasaRule.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.stories = RasaStory.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.entities = RasaEntity.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.slots = RasaSlot.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.responses = RasaResponse.objects.select_related('dataset').filter(dataset_id=dataset_id)
        self.form = RasaForm.objects.select_related('dataset').filter(dataset_id=dataset_id)

    def export_response_to_yaml(self, output_file='response.yaml'):
        """
        将指定数据集的RasaResponse模型数据导出
        """
        responses = self.responses
        if not responses.exists():
            print(f"数据集ID '{self.dataset_id}' 不存在或不包含任何响应数据")
            return False
            # 手动构建YAML内容
        lines = []
        lines.append("version: 3.1")
        lines.append("nlu:")
        for response in responses:
            examples = response.example if isinstance(response.example, list) else []
            lines.append(f"  {response.name}:")
            for example in examples:
                lines.append(f"    -text: {example}")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"数据集ID '{self.dataset_id}' 成功导出 {responses.count()} 个响应到 {output_file}")
        return True
    def export_nlu(self, output_file='nlu.yaml'):
        """
        将指定数据集ID的RasaIntent模型数据导出为Rasa训练数据格式的YAML文件

        Args:
            dataset_id (int): 数据集ID
            output_file (str): 输出文件路径，默认为'intent.yaml'
        """
        # 查询指定数据集ID下的所有意图和实体数据
        intents = self.intents
        entities = self.entities
        # 检查是否存在该数据集的意图
        if not intents.exists():
            print(f"数据集ID '{self.dataset_id}' 不存在或不包含任何意图数据")
            return False

        # 手动构建YAML内容
        lines = []
        lines.append("version: 3.1")
        lines.append("nlu:")

        for intent in intents:
            # 确保example字段是列表格式
            examples = intent.example if isinstance(intent.example, list) else []
            lines.append(f"  - intent: {intent.name}")
            lines.append("    examples: |")
            for example in examples:
                lines.append(f"      - {example}")
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"数据集ID '{self.dataset_id}' 成功导出 {intents.count()} 个意图到 {output_file}")
        return True

    def export_dataset_rules_to_yaml(self, output_file='rule.yaml'):
        """
        将指定数据集ID的RasaRule模型数据导出为Rasa训练数据格式的YAML文件

        Args:
            dataset_id (int): 数据集ID
            output_file (str): 输出文件路径，默认为'rule.yaml'
        """
        # 获取指定数据集ID下的所有规则数据
        rules = self.rules
        if not rules.exists():
            print(f"数据集ID '{self.dataset_id}' 不存在或不包含任何规则数据")
            return False
        lines = []
        lines.append("version: 3.1")
        lines.append("rules:")
        for rule in rules:
            steps = rule.steps if isinstance(rule.steps, list) else []
            lines.append(f"  - rule: {rule.name}")
            lines.append("    steps:")
            for step in steps:
                value_type = step.get('type', None)
                name = step.get('name', None)
                if not name:
                    continue
                if value_type == 'intent':
                    lines.append(f"      - intent: {name}")
                elif value_type == 'response':
                    lines.append(f"      - action: {name}")
                elif value_type == 'active_loop':
                    lines.append(f"      - active_loop: {name}")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"数据集ID '{self.dataset_id}' 成功导出 {rules.count()} 个规则到 {output_file}")
        return True

    def export_dataset_stories_to_yaml(self, output_file='story.yaml'):
        """
        将指定数据集ID的RasaStory模型数据导出为Rasa训练数据格式的YAML文件

        Args:
            dataset_id (int): 数据集ID
            output_file (str): 输出文件路径，默认为'story.yaml'
        """
        # 获取指定数据集ID下的所有故事数据
        stories = self.stories
        if not stories.exists():
            print(f"数据集ID '{self.dataset_id}' 不存在或不包含任何故事数据")
            return False

        lines = []
        lines.append("version: 3.1")
        lines.append("stories:")
        for story in stories:
            steps = story.steps if isinstance(story.steps, list) else []
            lines.append(f"- story: {story.name}")
            lines.append("  steps:")
            for step in steps:
                value_type = step.get('type', None)
                name = step.get('id', None)
                if value_type == 'intent':
                    lines.append(f"    - intent: {name}")
                elif value_type == 'response':
                    lines.append(f"    - action: {name}")
                elif value_type == 'slot':
                    lines.append(f"    - slot_was_set:")
                    lines.append(f"      - {name}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"数据集ID '{self.dataset_id}' 成功导出 {stories.count()} 个故事到 {output_file}")
        return True


    def export_domain_file(self, output_file='domain.yaml'):
        """
        将指定数据集ID的RasaDomain模型数据导出为Rasa训练数据格式的YAML文件

        Args:
            dataset_id (int): 数据集ID
            output_file (str): 输出文件路径，默认为'domain.yaml'
        """
        # 获取指定数据集ID下的所有领域数据
        intents = self.intents.values('name')
        entities = self.entities.values('name')
        slots = self.slots.values('name')
        responses = self.responses
        lines = []
        lines.append("version: 3.1")
        lines.append("intents:")
        for intent in intents:
            lines.append(f"  - {intent['name']}")
        lines.append("entities:")
        for entity in entities:
            lines.append(f"  - {entity['name']}")
        lines.append("responses:")
        for response in responses:
            lines.append(f"  - {response.name}")
            examples = response.example if isinstance(response.example, list) else []
            # 检查是否有非空的示例
            non_empty_examples = [ex for ex in examples if ex and str(ex).strip()]
            if non_empty_examples:
                lines.append("    - text:")
                for example in non_empty_examples:
                    lines.append(f"      - {example}")
            for example in examples:
                lines.append(f"      - {example}")

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"数据集ID '{self.dataset_id}' 成功导出 {intents.count()} 个意图、{entities.count()} 个实体、{responses.count()} 个响应到 {output_file}")
