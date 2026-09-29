# Cloudflare DNS MCP: implementation conventions

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Python 3.11+, Ruff target py311 and 100-column configuration; snake_case tool handlers. |
| **Where?** | pyproject.toml. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to preserve the implementation’s existing conventions at the change boundary. |
| **Why this approach?** | Python 3.11+, Ruff target py311 and 100-column configuration; snake_case tool handlers. |
| **Why it matters?** | Small compatible changes remain easier to review and recover. |

## Existing conventions

Python 3.11+, Ruff target py311 and 100-column configuration; snake_case tool handlers. Preserve optional-field mapping and explicit keyword SDK arguments. Add tests at the _call and fake-resource seams rather than use real DNS as a unit fixture. Do not generalize the ten-tool server into a full Cloudflare deployment platform without a requirement.

## Change boundary

One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. Handlers pass explicit zone/record arguments to SDK resources. _record_to_dict normalizes optional fields/timestamps. This deliberately small source layout is appropriate to ten tools; no recorded alternative architecture decision was found. Adding a separate database or control plane would need a demonstrated use case.

Prefer the smallest change in the component that already owns the behavior. Preserve generated artifacts and original requirements. Test a changed contract at its actual boundary; do not add scaffolding, services or broad refactors only to satisfy a documentation layout.

## Supporting sources

- [pyproject.toml](../../pyproject.toml)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
