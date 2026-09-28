# Cloudflare DNS MCP: executable interfaces

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Tools: list_zones(name_filter?); get_zone(zone_id); get_zone_settings(zone_id); list_dns_records(zone_id,record_type?,name?); get_dns_record(zone_id,record_id); create_dns_record(zone_id,record_type,name,content,ttl=1,proxied=False,priority?,comment?); update_dns_record(zone_id,record_id,content?,ttl?,proxied?,comment?); delete_dns_record(zone_id,record_id); purge_cache(zone_id,urls?,purge_everything=False); list_page_rules(zone_id,status?). |
| **Where?** | cf/server.py, tests/test_server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to prevent unsupported parameters or misleading success results from guiding an action. |
| **Why this approach?** | Tools: list_zones(name_filter?); get_zone(zone_id); get_zone_settings(zone_id); list_dns_records(zone_id,record_type?,name?); get_dns_record(zone_id,record_id); create_dns_record(zone_id,record_type,name,content,ttl=1,proxied=False,priority?,comment?); update_dns_record(zone_id,record_id,content?,ttl?,proxied?,comment?); delete_dns_record(zone_id,record_id); purge_cache(zone_id,urls?,purge_everything=False); list_page_rules(zone_id,status?). |
| **Why it matters?** | Zone ID and record ID define the target. |

## Exact current interface

Tools: list_zones(name_filter?); get_zone(zone_id); get_zone_settings(zone_id); list_dns_records(zone_id,record_type?,name?); get_dns_record(zone_id,record_id); create_dns_record(zone_id,record_type,name,content,ttl=1,proxied=False,priority?,comment?); update_dns_record(zone_id,record_id,content?,ttl?,proxied?,comment?); delete_dns_record(zone_id,record_id); purge_cache(zone_id,urls?,purge_everything=False); list_page_rules(zone_id,status?). Create uppercases type; update fetches the current record and sends its type/name plus supported fields. update does not expose record rename/type change/priority. Delete and whole-zone purge check CF_ALLOW_DESTRUCTIVE. Targeted purge needs 1..30 URLs; whole-zone mode overrides URLs. Errors return {error: message}. _call attempts five times on 429/500/502/503/504 with 1/2/4/8-second waits; other API errors become RuntimeError. stdio default, optional SSE at MCP_HOST=127.0.0.1 and MCP_PORT=3001.

## Complete registered signatures

These signatures are transcribed from the current Python handler definitions. Optional defaults are source behavior; effect labels distinguish configuration/authentication changes from reporting.

| Handler signature | Effect |
| --- | --- |
| `list_zones(name_filter: Optional[str]=None)` | provider read or local discovery |
| `get_zone(zone_id: str)` | provider read or local discovery |
| `get_zone_settings(zone_id: str)` | provider read or local discovery |
| `list_dns_records(zone_id: str, record_type: Optional[str]=None, name: Optional[str]=None)` | provider read or local discovery |
| `get_dns_record(zone_id: str, record_id: str)` | provider read or local discovery |
| `create_dns_record(zone_id: str, record_type: str, name: str, content: str, ttl: int=1, proxied: bool=False, priority: Optional[int]=None, comment: Optional[str]=None)` | external write |
| `update_dns_record(zone_id: str, record_id: str, content: Optional[str]=None, ttl: Optional[int]=None, proxied: Optional[bool]=None, comment: Optional[str]=None)` | external write |
| `delete_dns_record(zone_id: str, record_id: str)` | external write |
| `purge_cache(zone_id: str, urls: Optional[list[str]]=None, purge_everything: bool=False)` | external write |
| `list_page_rules(zone_id: str, status: Optional[str]=None)` | provider read or local discovery |

## Authorization and error limits

CF_ALLOW_DESTRUCTIVE accepts any nonempty environment value, including false. Creation, update and targeted cache purge are not covered by that guard. All are consequential operations requiring exact authorization. _call retries mutations as well as reads and supplies no idempotency key; uncertain create outcomes require duplicate checks rather than blanket re-execution. No additional SSE authentication is implemented in this source.

## Contract gaps

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

## Supporting sources

- [cf/server.py](../../cf/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
