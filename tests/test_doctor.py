import io
import json
import unittest
import urllib.error
from unittest.mock import patch

from doctor import Doctor, normalize_base_url, validate_chat_response


class FakeResponse:
    def __init__(self, body, status=200):
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size=-1):
        return self.body[:size]


class NormalizeUrlTests(unittest.TestCase):
    def test_trailing_slash(self):
        self.assertEqual(normalize_base_url("http://localhost:8000/v1/"), "http://localhost:8000/v1")

    def test_rejects_missing_scheme(self):
        with self.assertRaises(ValueError):
            normalize_base_url("localhost:8000/v1")

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            normalize_base_url("https://user:secret@example.com/v1")


class ResponseSchemaTests(unittest.TestCase):
    def test_valid_chat_response(self):
        ok, _ = validate_chat_response({"choices": [{"message": {"content": "OK"}}]})
        self.assertTrue(ok)

    def test_missing_choices(self):
        ok, detail = validate_chat_response({"id": "test"})
        self.assertFalse(ok)
        self.assertIn("choices", detail)

    def test_invalid_message(self):
        ok, _ = validate_chat_response({"choices": [{"message": None}]})
        self.assertFalse(ok)


class DoctorHttpTests(unittest.TestCase):
    def setUp(self):
        self.doctor = Doctor("https://proxy.example/v1", "test-key", "test-model")

    @patch("doctor.urllib.request.urlopen")
    def test_models_discovery_and_bearer_header(self, urlopen):
        urlopen.return_value = FakeResponse(json.dumps({"data": [{"id": "test-model"}]}))
        self.doctor.check_models()
        self.assertTrue(self.doctor.results[0].ok)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertTrue(request.full_url.endswith("/models"))

    @patch("doctor.urllib.request.urlopen")
    def test_chat_completion_success(self, urlopen):
        body = {"choices": [{"message": {"content": "OK"}}]}
        urlopen.return_value = FakeResponse(json.dumps(body))
        self.doctor.check_chat()
        self.assertTrue(self.doctor.results[0].ok)
        request = urlopen.call_args.args[0]
        self.assertTrue(request.full_url.endswith("/chat/completions"))
        self.assertFalse(json.loads(request.data)["stream"])

    @patch("doctor.urllib.request.urlopen")
    def test_streaming_success(self, urlopen):
        urlopen.return_value = FakeResponse('data: {"choices":[]}\\n\\ndata: [DONE]\\n\\n')
        self.doctor.check_chat(stream=True)
        self.assertTrue(self.doctor.results[0].ok)
        self.assertIn("(stream)", self.doctor.results[0].name)
        self.assertTrue(json.loads(urlopen.call_args.args[0].data)["stream"])

    @patch("doctor.urllib.request.urlopen")
    def test_streaming_rejects_missing_done_marker(self, urlopen):
        urlopen.return_value = FakeResponse('data: {"choices":[]}\\n\\n')
        self.doctor.check_chat(stream=True)
        self.assertFalse(self.doctor.results[0].ok)
        self.assertIn("[DONE]", self.doctor.results[0].detail)
        self.assertIn("(stream)", self.doctor.results[0].name)

    @patch("doctor.urllib.request.urlopen")
    def test_http_error_is_reported(self, urlopen):
        urlopen.side_effect = urllib.error.HTTPError(
            "https://proxy.example/v1/chat/completions", 401, "Unauthorized",
            hdrs=None, fp=io.BytesIO(b"invalid API key"))
        self.doctor.check_chat()
        self.assertFalse(self.doctor.results[0].ok)
        self.assertIn("HTTP 401", self.doctor.results[0].detail)

    @patch("doctor.urllib.request.urlopen")
    def test_timeout_is_reported(self, urlopen):
        urlopen.side_effect = TimeoutError()
        self.doctor.check_chat()
        self.assertFalse(self.doctor.results[0].ok)
        self.assertIn("timed out", self.doctor.results[0].detail)

    @patch.object(Doctor, "check_chat")
    def test_stream_option_runs_json_and_sse_checks(self, check_chat):
        self.doctor.verify_models = False
        with patch("builtins.print"):
            self.assertTrue(self.doctor.run(stream=True))
        self.assertEqual([call.args for call in check_chat.call_args_list], [(False,), (True,)])


if __name__ == "__main__":
    unittest.main()
