# Architecture — mcp-cloudflare-dns

## Component map

| Component | File | Role |
|---|---|---|
| MCP server | [`../cf/server.py`](../cf/server.py) | Declares every tool and returns normalized responses |
| Cloudflare client loader | [`../cf/server.py`](../cf/server.py) | Reads `CF_API_TOKEN` once and memoizes the client |
| Retry wrapper | [`../cf/server.py`](../cf/server.py) | Retries 429/5xx Cloudflare failures with backoff |
| Package metadata | [`../pyproject.toml`](../pyproject.toml) | Version, dependencies, script entry point |
| Registry metadata | [`../server.json`](../server.json) | External MCP registry description |

## Tool families

- Zone tools: inventory and settings inspection
- DNS tools: list, read, create, update, delete
- Edge actions: cache purge and page-rule inspection

## Lifecycle

1. The MCP client starts `mcp-cloudflare-dns`.
2. `FastMCP` registers the tool surface from `cf/server.py`.
3. The first tool call resolves `CF_API_TOKEN` and builds the Cloudflare SDK client.
4. Tool handlers call `_call()`, which retries retryable API failures.
5. Responses are normalized to plain dictionaries before returning to the MCP client.
