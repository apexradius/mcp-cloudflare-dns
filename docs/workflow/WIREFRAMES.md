# Cloudflare DNS MCP: task journeys

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Discover zone -> read exact record -> prepare minimal supported field change and recovery -> obtain applicable approval -> apply once -> read back record -> separately verify relevant DNS/user path. |
| **Where?** | README.md, cf/server.py, tests/test_server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to show the order of observations and actions required for a real task. |
| **Why this approach?** | Discover zone -> read exact record -> prepare minimal supported field change and recovery -> obtain applicable approval -> apply once -> read back record -> separately verify relevant DNS/user path. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Concrete interaction flow

Discover zone -> read exact record -> prepare minimal supported field change and recovery -> obtain applicable approval -> apply once -> read back record -> separately verify relevant DNS/user path. On an ambiguous create response, inspect for an already-created matching record before retrying; the generic retry wrapper is not duplicate prevention.

## Entry, result and failure states

The interface is tool schemas and zone/record summaries. Always show the intended record name/type, current versus proposed content, TTL/proxy change and exact zone before mutation. TTL documentation describes 1 as auto; actual provider acceptance must be validated for the exact record/proxy combination. Avoid presenting cache purge as DNS repair.

CF_ALLOW_DESTRUCTIVE accepts any nonempty environment value, including false. Creation, update and targeted cache purge are not covered by that guard. All are consequential operations requiring exact authorization. _call retries mutations as well as reads and supplies no idempotency key; uncertain create outcomes require duplicate checks rather than blanket re-execution. No additional SSE authentication is implemented in this source.

This is a sequence specification for the current interface. It does not introduce an unimplemented graphical application. Use the source tool/CLI contract for exact input fields.

## Supporting sources

- [README.md](../../README.md)
- [cf/server.py](../../cf/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
