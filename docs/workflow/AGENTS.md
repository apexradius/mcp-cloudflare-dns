# Cloudflare DNS MCP

## Product boundaries

Zone ID and record ID define the target. Read, create/update, delete and cache invalidation have different effects. A successful Admin API response is not proof of worldwide DNS propagation or restored user traffic.

## Read when needed

- Implementation changes: [CODE_STYLE.md](CODE_STYLE.md) and the affected source.
- Verification: [TESTING.md](TESTING.md).
- Contract/security questions: choose the relevant [INDEX.md](../../INDEX.md) route.
