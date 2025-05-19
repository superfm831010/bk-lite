# -- coding: utf-8 --
# @File: nast_request.py
# @Time: 2025/4/25 11:14
# @Author: windyzhao
# -- coding: utf-8 --
# @File: nats_client.py
# @Time: 2025/5/6
# @Author: windyzhao
import os
import asyncio
import nats
import json


class NATSClient:
    def __init__(self, server_url=None):
        if not server_url:
            server_url = os.getenv("NATS_URLS")
        self.server_url = server_url
        self.nc = None

    async def connect(self):
        """Connect to the NATS server."""
        self.nc = await nats.connect(self.server_url)

    async def request(self, subject, params, timeout=60):
        """
        Send a request to a NATS subject.

        :param subject: The subject to send the request to.
        :param params: The parameters to send in the request.
        :param timeout: Timeout for the request.
        :return: The response data.
        """
        if not self.nc:
            raise ConnectionError("NATS client is not connected.")
        
        payload = json.dumps(params).encode()
        response = await self.nc.request(subject, payload=payload, timeout=timeout)
        return json.loads(response.data.decode())

    async def close(self):
        """Close the connection to the NATS server."""
        if self.nc:
            await self.nc.drain()


# Example usage
async def main():
    client = NATSClient("")
    await client.connect()

    params = {
        "args": [
            {
                "command": "uname -a",
                "execute_timeout": 60
            }
        ],
        "kwargs": {}
    }
    subject = ""
    response = await client.request(subject, params)
    print(f"Received a message: {response}")

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())