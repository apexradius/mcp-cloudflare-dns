# Cloudflare DNS MCP: available capability boundaries

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Tools: list_zones(name_filter?); get_zone(zone_id); get_zone_settings(zone_id); list_dns_records(zone_id,record_type?,name?); get_dns_record(zone_id,record_id); create_dns_record(zone_id,record_type,name,content,ttl=1,proxied=False,priority?,comment?); update_dns_record(zone_id,record_id,content?,ttl?,proxied?,comment?); delete_dns_record(zone_id,record_id); purge_cache(zone_id,urls?,purge_everything=False); list_page_rules(zone_id,status?). |
| **Where?** | README.md, pyproject.toml, cf/server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to distinguish available implementation from authorized operation. |
| **Why this approach?** | Zone ID and record ID define the target. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Implemented surface

Tools: list_zones(name_filter?); get_zone(zone_id); get_zone_settings(zone_id); list_dns_records(zone_id,record_type?,name?); get_dns_record(zone_id,record_id); create_dns_record(zone_id,record_type,name,content,ttl=1,proxied=False,priority?,comment?); update_dns_record(zone_id,record_id,content?,ttl?,proxied?,comment?); delete_dns_record(zone_id,record_id); purge_cache(zone_id,urls?,purge_everything=False); list_page_rules(zone_id,status?). Create uppercases type; update fetches the current record and sends its type/name plus supported fields. update does not expose record rename/type change/priority. Delete and whole-zone purge check CF_ALLOW_DESTRUCTIVE. Targeted purge needs 1..30 URLs; whole-zone mode overrides URLs. Errors return {error: message}. _call attempts five times on 429/500/502/503/504 with 1/2/4/8-second waits; other API errors become RuntimeError. stdio default, optional SSE at MCP_HOST=127.0.0.1 and MCP_PORT=3001.

## Capability does not imply authorization

Zone ID and record ID define the target. Read, create/update, delete and cache invalidation have different effects. A successful Admin API response is not proof of worldwide DNS propagation or restored user traffic.

CF_ALLOW_DESTRUCTIVE accepts any nonempty environment value, including false. Creation, update and targeted cache purge are not covered by that guard. All are consequential operations requiring exact authorization. _call retries mutations as well as reads and supplies no idempotency key; uncertain create outcomes require duplicate checks rather than blanket re-execution. No additional SSE authentication is implemented in this source.

Route the current task through [the conductor selector](../../prompt.md#select-the-conductor). No native runtime, MCP connection, paid model, hook or third-party account is activated by this inventory. Verify availability in the actual invocation instead of inferring it from installed source.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [cf/server.py](../../cf/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
