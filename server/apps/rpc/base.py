import asyncio
import os

import nats_client


class RpcClient(object):
    def __init__(self):
        namespace = os.getenv("NATS_NAMESPACE", "bk_lite")
        self.namespace = namespace

    def run(self, method_name, *args, **kwargs):
        return_data = asyncio.run(nats_client.request(self.namespace, method_name, *args, **kwargs))
        return return_data
