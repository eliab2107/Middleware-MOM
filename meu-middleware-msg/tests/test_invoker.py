import pytest
import asyncio

from middleware.broker.broker_service import BrokerService
from middleware.broker.connection import BrokerConnection
from middleware.client.proxy import Proxy
from middleware.server.server_handler import ServerHandler
from app_demo.services import Calculator


@pytest.mark.asyncio
async def test_invoker_add():
    broker = BrokerService()
    conn = BrokerConnection(broker)
    srv = ServerHandler(broker, queue="requests")
    srv.register_service(Calculator())

    proxy = Proxy(conn, queue="requests")
    res = await proxy.call("add", 10, 5)
    assert res == 15
