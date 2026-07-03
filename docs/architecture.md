# Architecture

`mcp-cloudflare-dns` is a Python MCP server around Cloudflare zone administration. It keeps the
surface small: zones, records, cache purge, page rules, and settings.

## Components

```mermaid
flowchart TD
    Main[cf/server.py] --> Tools[MCP tools]
    Tools --> Env[Environment config]
    Tools --> Guard[Destructive guard]
    Tools --> Client[Cloudflare SDK client]

    Client --> Zones[Zone APIs]
    Client --> Records[DNS record APIs]
    Client --> Cache[Cache APIs]
    Client --> PageRules[Page Rules APIs]
```

## Request Sequence

```mermaid
sequenceDiagram
    actor User
    participant MCP as MCP client
    participant Server as cf/server.py
    participant Guard as Destructive guard
    participant CF as Cloudflare API

    User->>MCP: Ask to manage DNS
    MCP->>Server: Call MCP tool
    Server->>Guard: Check risk and env flag
    alt operation allowed
        Server->>CF: Run zone/DNS/cache request
        CF-->>Server: API response
        Server-->>MCP: Structured result
    else blocked
        Server-->>MCP: Safe refusal with reason
    end
```

## Data Boundaries

| Data | Source | Storage |
|---|---|---|
| Cloudflare API token | `CF_API_TOKEN` or `CLOUDFLARE_API_TOKEN` | Environment only. |
| Destructive mode | `CF_ALLOW_DESTRUCTIVE` | Environment only. |
| Zone/record data | Cloudflare API | Returned through MCP; not persisted here. |

## Extension Points

| Change | File |
|---|---|
| Add a new Cloudflare tool | `cf/server.py` |
| Change destructive safety rules | `cf/server.py` |
| Add package metadata | `pyproject.toml` |
