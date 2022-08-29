from microvoicemaster import APP
from microvoicemaster.transport.endpoints import Endpoint
from chrdiotypes.musical import CheetSheet
from .strategies import chsh_strategies
from fastapi.testclient import TestClient
from hypothesis import given, strategies as st

# Tests provide no remote server connection,
# hence ignoring the server exceptions
TEST_APP = TestClient(APP, raise_server_exceptions=False)

@given(**chsh_strategies)
def test_perform_200(info, structures, special_cases, bases, key, ordering):
    chsh = CheetSheet(info=info, structures=structures, special_cases=special_cases, bases=bases, key=key, ordering=ordering)
    payload = chsh.json()
    response = TEST_APP.post('/perform', payload)
    assert response.status_code == 200

def test_endpoint_builder():
    raw = """{"name": "microaccountant/music","host": "127.0.0.1","port": "8004","path": "ensure/music"}"""
    ep = Endpoint.parse_raw(raw)
    ep.option = "5"
    assert str(ep)