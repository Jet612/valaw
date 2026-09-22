import json
import unittest
from unittest.mock import AsyncMock

from valaw.client import Client, Exceptions, verify_content
from valaw.objects import AccountDto


class FakeResponse:
    def __init__(self, *, status=200, content_type="application/json", payload=None, text=""):
        self.status = status
        self.headers = {"Content-Type": content_type} if content_type is not None else {}
        self.payload = payload
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    async def json(self, *, content_type=None):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload

    async def text(self):
        return self._text


class FakeSession:
    def __init__(self, response):
        self.closed = False
        self.response = response

    def get(self, url, *, headers):
        return self.response


class VerifyContentTests(unittest.IsolatedAsyncioTestCase):
    async def test_parses_json_content_type_with_charset(self):
        response = FakeResponse(
            content_type="Application/JSON; Charset=UTF-8",
            payload={"ok": True},
        )

        self.assertEqual(await verify_content(response), {"ok": True})

    async def test_parses_json_body_when_content_type_is_missing(self):
        response = FakeResponse(content_type=None, text='{"ok": true}')

        self.assertEqual(await verify_content(response), {"ok": True})

    async def test_wraps_json_decode_errors(self):
        decode_error = json.JSONDecodeError("invalid", "{", 1)
        response = FakeResponse(payload=decode_error)

        with self.assertRaises(Exceptions.FailedToParseJSON) as raised:
            await verify_content(response)

        self.assertIs(raised.exception.__cause__, decode_error)


class ClientRequestTests(unittest.IsolatedAsyncioTestCase):
    async def test_raises_api_error_from_json_payload(self):
        client = Client("token", "americas")
        client.session = FakeSession(
            FakeResponse(
                status=429,
                payload={"status": {"message": "rate limited"}},
            )
        )

        with self.assertRaises(Exceptions.RiotAPIResponseError) as raised:
            await client._request("https://example.test", {})

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.status_message, "rate limited")

    async def test_uses_plain_text_for_non_json_api_error(self):
        client = Client("token", "americas")
        client.session = FakeSession(
            FakeResponse(
                status=502,
                content_type="text/plain",
                text="upstream unavailable",
            )
        )

        with self.assertRaises(Exceptions.RiotAPIResponseError) as raised:
            await client._request("https://example.test", {})

        self.assertEqual(raised.exception.status_code, 502)
        self.assertEqual(raised.exception.status_message, "upstream unavailable")

    async def test_decodes_typed_response_with_current_dataclass_wizard(self):
        client = Client("token", "americas")
        client._request = AsyncMock(
            return_value={"puuid": "player-id", "gameName": "Player", "tagLine": "NA1"}
        )

        account = await client.GET_getByRiotId("Player Name", "NA#1")

        self.assertEqual(
            account,
            AccountDto(puuid="player-id", gameName="Player", tagLine="NA1"),
        )
        request_url = client._request.await_args.args[0]
        self.assertTrue(request_url.endswith("/by-riot-id/Player%20Name/NA%231"))


if __name__ == "__main__":
    unittest.main()
