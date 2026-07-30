import pytest

from sma_ennexos.utils import _asdict, _b64url, generate_pkce, random_str


class TestBase64:
    def test_b64url_no_padding(self):
        result = _b64url(b"test")
        assert "=" not in result
        assert isinstance(result, str)

    def test_b64url_deterministic(self):
        assert _b64url(b"hello") == _b64url(b"hello")


class TestPKCE:
    def test_generate_pkce_returns_tuple(self):
        verifier, challenge = generate_pkce()
        assert isinstance(verifier, str)
        assert isinstance(challenge, str)
        assert len(verifier) > 0
        assert len(challenge) > 0

    def test_generate_pkce_different_each_time(self):
        v1, c1 = generate_pkce()
        v2, c2 = generate_pkce()
        assert v1 != v2
        assert c1 != c2


class TestRandomStr:
    def test_random_str_length(self):
        result = random_str()
        assert len(result) > 0
        assert isinstance(result, str)

    def test_random_str_unique(self):
        assert random_str() != random_str()


class TestAsdict:
    def test_skips_none(self):
        from dataclasses import dataclass

        @dataclass
        class Foo:
            a: str | None = None
            b: str = "keep"

        result = _asdict(Foo(b="bar"))
        assert "a" not in result
        assert result["b"] == "bar"

    def test_calls_to_dict_on_nested(self):
        from dataclasses import dataclass

        class _ToDict:
            def to_dict(self):
                return {"x": 1}

        @dataclass
        class Bar:
            inner: _ToDict | None = None

        result = _asdict(Bar(inner=_ToDict()))
        assert result["inner"] == {"x": 1}
