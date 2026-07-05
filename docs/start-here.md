# Start Here — mcp-cloudflare-dns

## What this repo ships

- One Python package: `mcp-cloudflare-dns`
- One MCP server entry point: `cf.server:main`
- One tool surface for Cloudflare zones, DNS records, cache purge, and page rules

## First run

1. Install the package:

```bash
python -m pip install mcp-cloudflare-dns
```

2. Export a token:

```bash
export CF_API_TOKEN="your-cloudflare-api-token"
```

3. Start it from an MCP client with `uvx mcp-cloudflare-dns`, or run it inside your own Python
environment with the same env var present.

## Required environment

| Variable | Required | Notes |
|---|---|---|
| `CF_API_TOKEN` | yes | Primary Cloudflare token name |
| `CLOUDFLARE_API_TOKEN` | optional | Alternate token name accepted by the server |
| `CF_ALLOW_DESTRUCTIVE` | optional | Required for destructive record or cache actions |
| `MCP_TRANSPORT` | optional | `stdio` by default; use `sse` for remote hosting |
| `MCP_HOST` / `MCP_PORT` | optional | SSE bind address when remote transport is enabled |

## Validation commands

```bash
python -m compileall cf
python -m build
```

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `CF_API_TOKEN not set` | Env var missing | Export the token before launch |
| Cloudflare 403/401 | Token scope too narrow | Add Zone DNS / Zone Read / Cache Purge permissions |
| Destructive tool refuses to run | Safety flag missing | Set `CF_ALLOW_DESTRUCTIVE=true` intentionally |
