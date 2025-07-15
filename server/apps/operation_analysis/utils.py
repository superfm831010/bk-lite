import asyncio
from nats.aio.client import Client as NATS


async def discover_services():
    nc = NATS()
    await nc.connect(servers=["nats://admin:5FE2MUTR7ZaLRVx7uAuObRnmBYxMG@10.10.41.149:4222"])

    # 查询所有服务
    response = await nc.request("$SRV.INFO", b"", timeout=1)
    print("Services:", response.data.decode())

    # 查询特定命名空间(app1)的服务
    response = await nc.request("$SRV.INFO.app1", b"", timeout=1)
    print("app1 Services:", response.data.decode())

    # 查询接口A的详细信息
    response = await nc.request("$SRV.INFO.app1.A", b"", timeout=1)
    print("Interface A details:", response.data.decode())

    # 查询接口B的详细信息
    response = await nc.request("$SRV.INFO.app1.B", b"", timeout=1)
    print("Interface B details:", response.data.decode())

    await nc.close()


asyncio.run(discover_services())