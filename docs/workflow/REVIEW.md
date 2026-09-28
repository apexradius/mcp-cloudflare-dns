# Cloudflare DNS MCP: documentation review continuity

Observed 2026-09-28 against source baseline `3b6b4f25fa52b1b4e7b9ec2c282503c3c7deed61`. This is a bounded continuity check of the earlier independent source review, not a new runtime or product acceptance test.

The 6 primary-source hashes recorded in the prior review still match this candidate baseline. The project-specific role bodies are retained; this change adds portable navigation, an actual-source map, a domain glossary and executable document checks. Historical/local-only references remain explicitly unavailable rather than being invented or silently imported.

## Previously source-challenged scenarios

### Update an MX priority while preserving other record fields

Reader recovery: API correctly exposes priority only on create, not update. Update fetches current type/name then sends supported content/ttl/proxied/comment fields; no priority/rename input exists. Recover a scoped interface change, not pretend content changes priority.

Source and dossier evidence: ["cf/server.py:create_dns_record", "cf/server.py:update_dns_record", "docs/workflow/API.md"]

Result: pass

Evidence level: inspected

### Retry a timed-out DNS create with destructive flag false

Reader recovery: _call can replay retryable provider errors across mutations without idempotency; no durable journal. False string is truthy only for delete/whole-zone purge; create/update/targeted purge remain external writes. Observe exact target/possible completion before retry and preserve recovery image.

Source and dossier evidence: ["cf/server.py:_call", "cf/server.py:delete_dns_record", "cf/server.py:purge_cache", "docs/workflow/API.md", "docs/workflow/DATABASE.md"]

Result: pass

Evidence level: inspected

## Source binding

| Source | SHA256 |
| --- | --- |
| `README.md` | `e7f66894bfe4d4158b896ea1560797a35f4fff4f1137e3924073ef45a2442cd1` |
| `pyproject.toml` | `1cc6a3e58ab9944ddcd14004b4e36b8216397262ac61783ab3bceae84ac3c9f0` |
| `cf/server.py` | `5150329af74d6df4d6d98a95aef4ce57568164f6a90407af5f0ee1ee8ab31cfc` |
| `tests/test_server.py` | `d7180adcf9ba93f2e380279197ef39582c8f8309a98f8f0fabf7b8ed8c7b70e3` |
| `docs/architecture.md` | `e1887bee1d38471bc035248676166dfd6bce845f2f454c23adda79115192d0ca` |
| `docs/start-here.md` | `f0c3d276fad2d77db683de64902bbfee7945f235d91c71425ee46f37a6e29155` |

Prior review artifact names: `tooling-independent-review.json`. The owner retains these in the dated 2026-09-26 reconstruction evidence directory. A fresh clone can inspect the above source and scenarios without that private directory.

## Limits

No new fresh-runtime comprehension, deployed behavior, provider operation or release is claimed. The current user request selects work; these scenarios are examples, not standing tasks. Local/CI/merge/knowledge status is recorded separately in review.json.
