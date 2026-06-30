import os
import time
from typing import Optional

import cloudflare
from cloudflare import APIError, APIStatusError
from fastmcp import FastMCP

mcp = FastMCP("mcp-cloudflare-dns")

_client: Optional[cloudflare.Cloudflare] = None

_RETRYABLE = {429, 500, 502, 503, 504}
_MAX_RETRIES = 5


def _get_client() -> cloudflare.Cloudflare:
    global _client
    if _client is None:
        token = os.environ.get("CF_API_TOKEN") or os.environ.get("CLOUDFLARE_API_TOKEN")
        if not token:
            raise RuntimeError(
                "CF_API_TOKEN not set. Export your Cloudflare API token before starting the server."
            )
        _client = cloudflare.Cloudflare(api_token=token)
    return _client


def _call(fn, *args, **kwargs):
    delay = 1.0
    for attempt in range(_MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except APIStatusError as e:
            if e.status_code not in _RETRYABLE or attempt == _MAX_RETRIES - 1:
                raise RuntimeError(f"Cloudflare API error {e.status_code}: {e.message}") from None
            time.sleep(delay)
            delay = min(delay * 2, 60)
        except APIError as e:
            raise RuntimeError(f"Cloudflare error: {e}") from None
    return None


def _err(e: Exception) -> dict:
    return {"error": str(e)}


def _record_to_dict(r) -> dict:
    return {
        "id": r.id,
        "name": r.name,
        "type": r.type,
        "content": r.content,
        "ttl": r.ttl,
        "proxied": getattr(r, "proxied", None),
        "comment": getattr(r, "comment", None),
        "created_on": str(r.created_on) if getattr(r, "created_on", None) else None,
        "modified_on": str(r.modified_on) if getattr(r, "modified_on", None) else None,
    }


# ---------------------------------------------------------------------------
# Zone tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_zones(name_filter: Optional[str] = None) -> list[dict]:
    """
    List all Cloudflare zones on this account.

    Args:
        name_filter: Optional domain name substring to filter results (e.g. 'example.com')
    """
    try:
        cf = _get_client()
        kwargs = {}
        if name_filter:
            kwargs["name"] = name_filter
        zones = _call(cf.zones.list, **kwargs)
        return [
            {
                "id": z.id,
                "name": z.name,
                "status": z.status,
                "plan": z.plan.name if z.plan else None,
                "nameservers": list(z.name_servers) if z.name_servers else [],
                "paused": z.paused,
                "account": z.account.name if z.account else None,
            }
            for z in zones
        ]
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_zone(zone_id: str) -> dict:
    """Get details for a specific Cloudflare zone by ID."""
    try:
        cf = _get_client()
        z = _call(cf.zones.get, zone_id=zone_id)
        return {
            "id": z.id,
            "name": z.name,
            "status": z.status,
            "plan": z.plan.name if z.plan else None,
            "nameservers": list(z.name_servers) if z.name_servers else [],
            "original_nameservers": list(z.original_name_servers) if z.original_name_servers else [],
            "paused": z.paused,
            "type": z.type,
            "created_on": str(z.created_on) if z.created_on else None,
            "modified_on": str(z.modified_on) if z.modified_on else None,
            "activated_on": str(z.activated_on) if z.activated_on else None,
        }
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_zone_settings(zone_id: str) -> dict:
    """
    Get key security and performance settings for a zone.
    Returns SSL mode, security level, minification, always-https, brotli, etc.
    """
    try:
        cf = _get_client()
        settings = _call(cf.zones.settings.get, zone_id=zone_id)
        result = {}
        for item in settings.result if hasattr(settings, "result") else []:
            result[item.id] = item.value
        return result
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# DNS record tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_dns_records(
    zone_id: str,
    record_type: Optional[str] = None,
    name: Optional[str] = None,
) -> list[dict]:
    """
    List DNS records for a zone.

    Args:
        zone_id: Cloudflare zone ID
        record_type: Filter by type — A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, etc.
        name: Filter by record name (e.g. 'api.example.com')
    """
    try:
        cf = _get_client()
        kwargs = {"zone_id": zone_id}
        if record_type:
            kwargs["type"] = record_type
        if name:
            kwargs["name"] = name
        records = _call(cf.dns.records.list, **kwargs)
        return [_record_to_dict(r) for r in records]
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_dns_record(zone_id: str, record_id: str) -> dict:
    """Get a specific DNS record by zone ID and record ID."""
    try:
        cf = _get_client()
        r = _call(cf.dns.records.get, dns_record_id=record_id, zone_id=zone_id)
        return _record_to_dict(r)
    except Exception as e:
        return _err(e)


@mcp.tool()
def create_dns_record(
    zone_id: str,
    record_type: str,
    name: str,
    content: str,
    ttl: int = 1,
    proxied: bool = False,
    priority: Optional[int] = None,
    comment: Optional[str] = None,
) -> dict:
    """
    Create a new DNS record.

    Args:
        zone_id: Cloudflare zone ID
        record_type: A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, etc.
        name: Record name (e.g. 'api' or 'api.example.com')
        content: Record value (IP address, hostname, text, etc.)
        ttl: TTL in seconds. 1 = auto (only valid when proxied=True)
        proxied: Whether to proxy through Cloudflare (orange cloud). Only valid for A, AAAA, CNAME.
        priority: MX/SRV priority (required for MX records)
        comment: Optional note about this record
    """
    try:
        cf = _get_client()
        kwargs = {
            "zone_id": zone_id,
            "type": record_type.upper(),
            "name": name,
            "content": content,
            "ttl": ttl,
        }
        if proxied:
            kwargs["proxied"] = proxied
        if priority is not None:
            kwargs["priority"] = priority
        if comment:
            kwargs["comment"] = comment
        r = _call(cf.dns.records.create, **kwargs)
        return _record_to_dict(r)
    except Exception as e:
        return _err(e)


@mcp.tool()
def update_dns_record(
    zone_id: str,
    record_id: str,
    content: Optional[str] = None,
    ttl: Optional[int] = None,
    proxied: Optional[bool] = None,
    comment: Optional[str] = None,
) -> dict:
    """
    Update an existing DNS record. Only the fields you provide will be changed.

    Args:
        zone_id: Cloudflare zone ID
        record_id: DNS record ID to update
        content: New record value
        ttl: New TTL in seconds (1 = auto)
        proxied: Toggle Cloudflare proxy on/off
        comment: Update the record comment
    """
    try:
        cf = _get_client()
        # Fetch current record first to fill required fields
        current = _call(cf.dns.records.get, dns_record_id=record_id, zone_id=zone_id)
        kwargs = {
            "zone_id": zone_id,
            "dns_record_id": record_id,
            "type": current.type,
            "name": current.name,
            "content": content if content is not None else current.content,
            "ttl": ttl if ttl is not None else current.ttl,
        }
        if proxied is not None:
            kwargs["proxied"] = proxied
        elif getattr(current, "proxied", None) is not None:
            kwargs["proxied"] = current.proxied
        if comment is not None:
            kwargs["comment"] = comment
        r = _call(cf.dns.records.update, **kwargs)
        return _record_to_dict(r)
    except Exception as e:
        return _err(e)


@mcp.tool()
def delete_dns_record(zone_id: str, record_id: str) -> dict:
    """
    Delete a DNS record. Requires CF_ALLOW_DESTRUCTIVE=true.

    Args:
        zone_id: Cloudflare zone ID
        record_id: DNS record ID to delete
    """
    if not os.environ.get("CF_ALLOW_DESTRUCTIVE"):
        return {"error": "DNS record deletion is disabled. Set CF_ALLOW_DESTRUCTIVE=true to enable."}
    try:
        cf = _get_client()
        _call(cf.dns.records.delete, dns_record_id=record_id, zone_id=zone_id)
        return {"success": True, "deleted": record_id}
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Cache tools
# ---------------------------------------------------------------------------

@mcp.tool()
def purge_cache(
    zone_id: str,
    urls: Optional[list[str]] = None,
    purge_everything: bool = False,
) -> dict:
    """
    Purge Cloudflare cache for a zone.

    Args:
        zone_id: Cloudflare zone ID
        urls: Specific URLs to purge (up to 30 per call)
        purge_everything: Purge entire zone cache (overrides urls). Requires CF_ALLOW_DESTRUCTIVE=true.
    """
    if purge_everything and not os.environ.get("CF_ALLOW_DESTRUCTIVE"):
        return {"error": "purge_everything requires CF_ALLOW_DESTRUCTIVE=true."}
    if not urls and not purge_everything:
        return {"error": "Provide urls to purge or set purge_everything=true."}
    try:
        cf = _get_client()
        if purge_everything:
            _call(cf.cache.purge, zone_id=zone_id, purge_everything=True)
            return {"success": True, "purged": "everything"}
        else:
            if len(urls) > 30:
                return {"error": "Maximum 30 URLs per purge call. Split into batches."}
            _call(cf.cache.purge, zone_id=zone_id, files=urls)
            return {"success": True, "purged": urls}
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Page rules
# ---------------------------------------------------------------------------

@mcp.tool()
def list_page_rules(zone_id: str, status: Optional[str] = None) -> list[dict]:
    """
    List page rules for a zone.

    Args:
        zone_id: Cloudflare zone ID
        status: Filter by 'active' or 'disabled' (default: all)
    """
    try:
        cf = _get_client()
        kwargs = {"zone_id": zone_id}
        if status:
            kwargs["status"] = status
        rules = _call(cf.page_rules.list, **kwargs)
        return [
            {
                "id": r.id,
                "status": r.status,
                "priority": r.priority,
                "targets": [
                    {"target": t.target, "constraint": {"operator": t.constraint.operator, "value": t.constraint.value}}
                    for t in (r.targets or [])
                ],
                "actions": [
                    {"id": a.id, "value": a.value}
                    for a in (r.actions or [])
                ],
                "modified_on": str(r.modified_on) if r.modified_on else None,
            }
            for r in (rules or [])
        ]
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "3001"))
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
