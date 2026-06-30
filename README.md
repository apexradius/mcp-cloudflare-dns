# mcp-cloudflare-dns

Cloudflare DNS MCP server. Manage zones, DNS records, cache, and page rules from Claude, Cursor, Codex, or any MCP-compatible AI assistant.

```
# Install:  uvx mcp-cloudflare-dns

# Ask your AI:
"List all DNS records for example.com"
"Add a CNAME record pointing api.example.com to my-app.vercel.app"
"Purge the cache for https://example.com/products"
"What page rules are active on example.com?"
```

---

## Why this one?

The official Cloudflare MCP covers Workers, KV, D1, and R2 — but has **zero DNS tools**. This server fills that gap.

| Feature | This server | Official CF MCP |
|---|---|---|
| DNS record CRUD | Yes | No |
| Zone listing | Yes | No |
| Cache purge | Yes | No |
| Page rules | Yes | No |
| Zone settings | Yes | No |
| Workers/KV/D1/R2 | No | Yes |

They complement each other — use both.

---

## Quickstart

**1. Get a Cloudflare API token** — [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens) → Create Token → use "Edit zone DNS" template

**2. Add to your MCP client config:**

```json
{
  "mcpServers": {
    "cloudflare-dns": {
      "command": "uvx",
      "args": ["mcp-cloudflare-dns"],
      "env": {
        "CF_API_TOKEN": "your-cloudflare-api-token"
      }
    }
  }
}
```

**3. Restart your AI client. Done.**

---

## Available tools

| Tool | What it does |
|---|---|
| `list_zones` | All zones on your account with status and nameservers |
| `get_zone` | Details for a specific zone |
| `get_zone_settings` | SSL mode, security level, minification, HTTPS redirect, etc. |
| `list_dns_records` | All DNS records, filterable by type or name |
| `get_dns_record` | Single record by ID |
| `create_dns_record` | Add A, AAAA, CNAME, MX, TXT, NS, etc. |
| `update_dns_record` | Edit content, TTL, proxy status, or comment |
| `delete_dns_record` | Remove a record *(requires `CF_ALLOW_DESTRUCTIVE=true`)* |
| `purge_cache` | Purge specific URLs or entire zone cache |
| `list_page_rules` | All page rules with targets and actions |

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `CF_API_TOKEN` | Yes | Cloudflare API token (also accepts `CLOUDFLARE_API_TOKEN`) |
| `CF_ALLOW_DESTRUCTIVE` | No | Set to `true` to enable record deletion and full cache purge |
| `MCP_TRANSPORT` | No | Set to `sse` for remote/VPS deployment (default: `stdio`) |
| `MCP_HOST` | No | SSE bind host (default: `127.0.0.1`) |
| `MCP_PORT` | No | SSE bind port (default: `3001`) |

---

## API token permissions

Minimum required scopes for your token:

| Resource | Permission |
|---|---|
| Zone — DNS | Edit |
| Zone — Zone | Read |
| Zone — Cache Purge | Purge |
| Zone — Page Rules | Edit *(if using page rules tools)* |

---

## License

MIT

<!-- mcp-name: io.github.Ayo-Fam/mcp-cloudflare-dns -->
