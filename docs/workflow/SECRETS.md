# Cloudflare DNS MCP: configuration and private inputs

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | CF_API_TOKEN or CLOUDFLARE_API_TOKEN supplies the credential; document required zone/API scope and storage owner without the token. |
| **Where?** | cf/server.py, tests/test_server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to resolve configuration responsibility without exposing values. |
| **Why this approach?** | CF_API_TOKEN or CLOUDFLARE_API_TOKEN supplies the credential; document required zone/API scope and storage owner without the token. |
| **Why it matters?** | Private input access is not necessary to understand the product contract. |

## Metadata-only configuration map

CF_API_TOKEN or CLOUDFLARE_API_TOKEN supplies the credential; document required zone/API scope and storage owner without the token. The server does not need a repository .env containing values. Zone and record identifiers can also be sensitive operational metadata; keep bounded receipts private where appropriate.

## Access discipline

This document carries configuration names, purpose and responsibility only. Never paste values, tokens, private prompts, unrestricted provider output or account exports. For a real credential failure, identify the approved storage/rotation path without printing its contents; verify the authorized replacement in the actual runtime and retain a redacted receipt. Secret presence, file readability and connector access are not approval to perform the task.

## Supporting sources

- [cf/server.py](../../cf/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
