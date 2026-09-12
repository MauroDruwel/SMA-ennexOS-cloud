from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from sma_ennexos_cloud import SmaClient
from sma_ennexos_cloud.auth import _parse_form_action, login, refresh_access_token
from sma_ennexos_cloud.exceptions import AuthenticationError


class TestParseFormAction:
    def test_finds_action(self):
        html = '<form method="post" action="/auth/login">'
        assert _parse_form_action(html) == "/auth/login"

    def test_returns_none_without_form(self):
        assert _parse_form_action("<html></html>") is None

    def test_handles_double_quotes(self):
        html = '<form action="/login">'
        assert _parse_form_action(html) == "/login"

    def test_handles_single_quotes(self):
        html = "<form action='/login'>"
        assert _parse_form_action(html) == "/login"


class TestLoginFlow:
    def test_successful_login(self):
        client = SmaClient(username="user", password="pwd")
        mock_get_resp = MagicMock()
        mock_get_resp.text = '<form action="/login">'

        mock_post_login_resp = MagicMock()
        mock_post_login_resp.headers = {"Location": "https://localhost/callback?code=testcode123"}

        mock_post_token_resp = MagicMock()
        mock_post_token_resp.json.return_value = {
            "access_token": "token_abc",
            "refresh_token": "refresh_xyz",
        }

        client._http.get = MagicMock(return_value=mock_get_resp)
        client._http.post = MagicMock(side_effect=[mock_post_login_resp, mock_post_token_resp])

        login(client)
        assert client.access_token == "token_abc"
        assert client.refresh_token == "refresh_xyz"

    def test_login_no_form(self):
        client = SmaClient(username="user", password="pwd")
        mock_get_resp = MagicMock()
        mock_get_resp.text = "<html>No form here</html>"
        client._http.get = MagicMock(return_value=mock_get_resp)

        with pytest.raises(AuthenticationError, match="Could not find login form"):
            login(client)

    def test_login_no_redirect(self):
        client = SmaClient(username="user", password="pwd")
        mock_get_resp = MagicMock()
        mock_get_resp.text = '<form action="/login">'

        mock_post_login_resp = MagicMock()
        mock_post_login_resp.headers = {}
        client._http.get = MagicMock(return_value=mock_get_resp)
        client._http.post = MagicMock(return_value=mock_post_login_resp)

        with pytest.raises(AuthenticationError, match="No redirect after login"):
            login(client)

    def test_login_no_code_in_redirect(self):
        client = SmaClient(username="user", password="pwd")
        mock_get_resp = MagicMock()
        mock_get_resp.text = '<form action="/login">'

        mock_post_login_resp = MagicMock()
        mock_post_login_resp.headers = {"Location": "https://localhost/callback?error=invalid"}
        client._http.get = MagicMock(return_value=mock_get_resp)
        client._http.post = MagicMock(return_value=mock_post_login_resp)

        with pytest.raises(AuthenticationError, match="No auth code in redirect URL"):
            login(client)


class TestRefreshToken:
    def test_refresh_token_missing(self):
        client = SmaClient()
        with pytest.raises(AuthenticationError, match="No refresh token"):
            refresh_access_token(client)

    def test_refresh_token_success(self):
        client = SmaClient()
        client.refresh_token = "old_ref"
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "access_token": "new_acc",
            "refresh_token": "new_ref",
        }
        client._http.post = MagicMock(return_value=mock_resp)

        refresh_access_token(client)
        assert client.access_token == "new_acc"
        assert client.refresh_token == "new_ref"
