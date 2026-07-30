import pytest

from sma_ennexos import SmaClient
from sma_ennexos.exceptions import AuthenticationError


class TestSmaClient:
    def test_init(self):
        client = SmaClient(username="user", password="pass")
        assert client.username == "user"
        assert client.password == "pass"
        assert client.access_token is None
        assert client.refresh_token is None
        assert client.component_id is None

    def test_login_requires_credentials(self):
        client = SmaClient()
        with pytest.raises(ValueError, match="Username and password"):
            client.login()

    def test_api_headers_raises_if_not_logged_in(self):
        client = SmaClient(username="u", password="p")
        with pytest.raises(AuthenticationError, match="Not logged in"):
            client._api_headers()

    def test_close_idempotent(self):
        client = SmaClient()
        client.close()
        client.close()
