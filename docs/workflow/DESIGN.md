# Cloudflare DNS MCP: operator experience

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | The interface is tool schemas and zone/record summaries. |
| **Where?** | cf/server.py, tests/test_server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to make the human-facing contract explicit even when the interface is a CLI or MCP tool. |
| **Why this approach?** | The interface is tool schemas and zone/record summaries. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Operator experience

The interface is tool schemas and zone/record summaries. Always show the intended record name/type, current versus proposed content, TTL/proxy change and exact zone before mutation. TTL documentation describes 1 as auto; actual provider acceptance must be validated for the exact record/proxy combination. Avoid presenting cache purge as DNS repair.

## State and error presentation

Discover zone -> read exact record -> prepare minimal supported field change and recovery -> obtain applicable approval -> apply once -> read back record -> separately verify relevant DNS/user path. On an ambiguous create response, inspect for an already-created matching record before retrying; the generic retry wrapper is not duplicate prevention.

## Review standard

Review the actual interface changed: schema/error/citation output for tools, and visible rendered pages where this product creates a document or browser experience. Do not invent screen designs, visual tokens or customer flows that the product does not contain. User-facing success must name what succeeded and what remains unverified.

## Supporting sources

- [cf/server.py](../../cf/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
