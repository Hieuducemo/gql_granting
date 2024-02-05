import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_voyager():
   import main
   client = TestClient(main.app, raise_server_exceptions=False)   
   client.get(url="/voyager")