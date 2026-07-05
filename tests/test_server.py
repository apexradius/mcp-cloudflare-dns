"""Hermetic tests for the Cloudflare DNS MCP server.

No network calls and no real Cloudflare credentials are used. These cover the
seams that break silently: the set of tools the server advertises, the record
mapper, and the destructive-operation / missing-credential guards.
"""

import asyncio
import types
import unittest
from unittest import mock

from cf import server

EXPECTED_TOOLS = {
    "list_zones",
    "get_zone",
    "get_zone_settings",
    "list_dns_records",
    "get_dns_record",
    "create_dns_record",
    "update_dns_record",
    "delete_dns_record",
    "purge_cache",
    "list_page_rules",
}


class ToolRegistrationTests(unittest.TestCase):
    def test_server_exposes_expected_tools_with_schemas(self):
        tools = asyncio.run(server.mcp.list_tools())
        names = {t.name for t in tools}
        self.assertEqual(names, EXPECTED_TOOLS)
        for t in tools:
            self.assertIsInstance(t.parameters, dict, f"{t.name} has no schema")
            self.assertIn("properties", t.parameters, f"{t.name} schema missing properties")


class CredentialGuardTests(unittest.TestCase):
    def test_missing_token_raises_clean_error(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            server._client = None
            with self.assertRaises(RuntimeError) as ctx:
                server._get_client()
        self.assertIn("CF_API_TOKEN", str(ctx.exception))


class DestructiveGuardTests(unittest.TestCase):
    def test_delete_record_disabled_without_flag(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            result = server.delete_dns_record("zone123", "rec456")
        self.assertIn("error", result)
        self.assertIn("disabled", result["error"])

    def test_purge_everything_requires_flag(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            result = server.purge_cache("zone123", purge_everything=True)
        self.assertIn("error", result)
        self.assertIn("CF_ALLOW_DESTRUCTIVE", result["error"])

    def test_purge_requires_target(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            result = server.purge_cache("zone123")
        self.assertIn("error", result)


class RecordMapperTests(unittest.TestCase):
    def test_record_to_dict_maps_fields(self):
        record = types.SimpleNamespace(
            id="rec1",
            name="api.example.com",
            type="A",
            content="203.0.113.10",
            ttl=1,
            proxied=True,
            comment="edge",
            created_on="2026-01-01",
            modified_on="2026-01-02",
        )
        out = server._record_to_dict(record)
        self.assertEqual(out["id"], "rec1")
        self.assertEqual(out["name"], "api.example.com")
        self.assertEqual(out["type"], "A")
        self.assertEqual(out["content"], "203.0.113.10")
        self.assertEqual(out["proxied"], True)
        self.assertEqual(out["created_on"], "2026-01-01")

    def test_record_to_dict_tolerates_missing_optional_fields(self):
        record = types.SimpleNamespace(
            id="rec2", name="x.example.com", type="TXT", content="v=spf1", ttl=3600
        )
        out = server._record_to_dict(record)
        self.assertIsNone(out["proxied"])
        self.assertIsNone(out["comment"])
        self.assertIsNone(out["created_on"])


if __name__ == "__main__":
    unittest.main()
