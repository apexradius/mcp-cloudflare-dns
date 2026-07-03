# Start Here

This server exposes Cloudflare DNS, cache purge, zone settings, and page-rule operations through
MCP. It is intentionally scoped to DNS/admin gaps that the broader Cloudflare MCP server does not
cover.

## First Run

```bash
uvx mcp-cloudflare-dns
```

Add `CF_API_TOKEN` to the MCP client environment. Use a scoped token; do not paste account-global
credentials into config examples.

## Safe Operations

1. Create a token with the minimum scopes listed in the README.
2. Start without `CF_ALLOW_DESTRUCTIVE`.
3. Confirm read/list operations first.
4. Enable `CF_ALLOW_DESTRUCTIVE=true` only when delete/full-purge tools are intentional.

## Development Loop

```bash
uv sync
uv run ruff check .
uv run python -m cf.server
```

Tool registration and Cloudflare SDK calls live in `cf/server.py`.
