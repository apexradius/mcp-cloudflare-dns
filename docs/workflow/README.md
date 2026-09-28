# Cloudflare DNS MCP: orientation

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation. |
| **Where?** | README.md, pyproject.toml, cf/server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to recover the purpose and correct owning implementation before acting. |
| **Why this approach?** | One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Product and scope

Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation.

Zone ID and record ID define the target. Read, create/update, delete and cache invalidation have different effects. A successful Admin API response is not proof of worldwide DNS propagation or restored user traffic.

## Find the owning behavior

One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. Handlers pass explicit zone/record arguments to SDK resources. _record_to_dict normalizes optional fields/timestamps. This deliberately small source layout is appropriate to ten tools; no recorded alternative architecture decision was found. Adding a separate database or control plane would need a demonstrated use case.

Use [API](API.md) for the exact interface, [DATABASE](DATABASE.md) for state, [TESTING](TESTING.md) for proof and [HANDOFFS](HANDOFFS.md) for current uncertainty. [The root README](../../README.md) remains the original manual; known stale statements are preserved and explained here, not silently adopted.

## Current baseline

Initial 256099c on 2026-06-30 delivered ten tools; 86c9cbe bumped to 0.1.1 for ownership verification; July added guides/hermetic tests. Current main 3b6b4f2 is the September 16 CI-gate merge. That history does not prove a package is installed, service running or DNS change pending.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [cf/server.py](../../cf/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
