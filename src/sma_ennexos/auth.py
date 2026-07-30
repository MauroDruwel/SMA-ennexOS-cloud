"""PKCE OAuth2 authentication for SMA ennexOS / Sunny Portal."""
from __future__ import annotations

import re
import urllib.parse
from typing import TYPE_CHECKING

from requests import Session

from .constants import (
    AUTH_PAGE_HEADERS,
    AUTH_URL,
    CLIENT_ID,
    LOGIN_POST_HEADERS,
    REDIRECT_URI,
    TOKEN_POST_HEADERS,
    TOKEN_URL,
)
from .exceptions import AuthenticationError
from .utils import generate_pkce, random_str

if TYPE_CHECKING:
    from .client import SmaClient


def login(client: SmaClient) -> None:
    """Perform the full PKCE OAuth2 login flow."""
    session = client._http
    code_verifier, code_challenge = generate_pkce()
    state = random_str()
    nonce = random_str()

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "nonce": nonce,
    }

    r = session.get(AUTH_URL, params=params, headers=AUTH_PAGE_HEADERS)
    r.raise_for_status()

    form_action = _parse_form_action(r.text)
    if not form_action:
        raise AuthenticationError("Could not find login form in the auth page")

    form_url = urllib.parse.urljoin(AUTH_URL, form_action)
    r2 = session.post(
        form_url,
        data={
            "username": client.username,
            "password": client.password,
            "credentialId": "",
        },
        headers=LOGIN_POST_HEADERS,
        allow_redirects=False,
    )
    r2.raise_for_status()

    location = r2.headers.get("Location")
    if not location:
        raise AuthenticationError(
            "No redirect after login – check credentials"
        )

    parsed = urllib.parse.urlparse(location)
    qs = urllib.parse.parse_qs(parsed.query)
    auth_code = qs.get("code", [None])[0]
    if not auth_code:
        raise AuthenticationError(
            f"No auth code in redirect URL: {location}"
        )

    r3 = session.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier,
            "client_id": CLIENT_ID,
        },
        headers=TOKEN_POST_HEADERS,
    )
    r3.raise_for_status()
    token_data = r3.json()
    client.access_token = token_data["access_token"]
    client.refresh_token = token_data.get("refresh_token")


def refresh_access_token(client: SmaClient) -> None:
    """Refresh the access token using the stored refresh token."""
    if not client.refresh_token:
        raise AuthenticationError("No refresh token available – login again")

    r = client._http.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": client.refresh_token,
            "client_id": CLIENT_ID,
        },
        headers=TOKEN_POST_HEADERS,
    )
    r.raise_for_status()
    token_data = r.json()
    client.access_token = token_data["access_token"]
    if "refresh_token" in token_data:
        client.refresh_token = token_data["refresh_token"]


def _parse_form_action(html: str) -> str | None:
    m = re.search(
        r'<form[^>]*\saction=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    return m.group(1) if m else None
