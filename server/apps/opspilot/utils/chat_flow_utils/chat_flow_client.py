class ChatFlowClient(object):
    def __init__(self, instance):
        self.instance = instance
        self.parse_chat_flow_json(instance.json_data)

    def parse_chat_flow_json(self, json_data):
        pass
