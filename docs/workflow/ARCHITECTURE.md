# Cloudflare DNS MCP: components and decisions

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. |
| **Where?** | cf/server.py, tests/test_server.py, docs/architecture.md. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to locate the component that owns the requested behavior. |
| **Why this approach?** | One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Components, flow and rationale

One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. Handlers pass explicit zone/record arguments to SDK resources. _record_to_dict normalizes optional fields/timestamps. This deliberately small source layout is appropriate to ten tools; no recorded alternative architecture decision was found. Adding a separate database or control plane would need a demonstrated use case.

## State boundary

No application database or durable operation journal is implemented. Client credentials live in environment; SDK results are mapped to dictionaries. DNS outputs include id,name,type,content,ttl,proxied,comment and timestamps. Before a later authorized change, retain a narrowly scoped recoverable before-image in an appropriate private task artifact; do not mistake this recommended operator practice for an existing transactional rollback implementation.

## Evolution and current mismatch

Initial 256099c on 2026-06-30 delivered ten tools; 86c9cbe bumped to 0.1.1 for ownership verification; July added guides/hermetic tests. Current main 3b6b4f2 is the September 16 CI-gate merge. That history does not prove a package is installed, service running or DNS change pending.

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

## Supporting sources

- [cf/server.py](../../cf/server.py)
- [tests/test_server.py](../../tests/test_server.py)
- [docs/architecture.md](../../docs/architecture.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
