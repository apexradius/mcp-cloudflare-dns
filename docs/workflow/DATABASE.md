# Cloudflare DNS MCP: state and persistence

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | No application database or durable operation journal is implemented. |
| **Where?** | README.md, pyproject.toml, cf/server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to identify what persists, what is transient and what requires recovery. |
| **Why this approach?** | No application database or durable operation journal is implemented. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Actual state model

No application database or durable operation journal is implemented. Client credentials live in environment; SDK results are mapped to dictionaries. DNS outputs include id,name,type,content,ttl,proxied,comment and timestamps. Before a later authorized change, retain a narrowly scoped recoverable before-image in an appropriate private task artifact; do not mistake this recommended operator practice for an existing transactional rollback implementation.

## State transition and recovery

Entrypoint cf.server:main. Resolve CF_API_TOKEN first, falling back to CLOUDFLARE_API_TOKEN. The SDK client is cached, so credential changes do not automatically prove the running process picked them up. No runtime was started here. Recovery for DNS uses the exact saved record state; cache purge cannot be undone by restoring a local file.

## Private-input boundary

CF_API_TOKEN or CLOUDFLARE_API_TOKEN supplies the credential; document required zone/API scope and storage owner without the token. The server does not need a repository .env containing values. Zone and record identifiers can also be sensitive operational metadata; keep bounded receipts private where appropriate.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [cf/server.py](../../cf/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
