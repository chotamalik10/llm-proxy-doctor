import unittest
from doctor import normalize_base_url, validate_chat_response

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

if __name__ == "__main__":
    unittest.main()
