import pytest
import requests

from sma_ennexos.auth import _parse_form_action, login, refresh_access_token
from sma_ennexos import SmaClient


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
