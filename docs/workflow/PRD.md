# Cloudflare DNS MCP: requirements and value

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Expose the ten implemented tools and return structured errors for missing credentials and provider failures. |
| **Where?** | README.md. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to keep implementation choices tied to the promised outcome. |
| **Why this approach?** | Expose the ten implemented tools and return structured errors for missing credentials and provider failures. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Vision and user value

Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation.

## Requirements and acceptance meaning

Expose the ten implemented tools and return structured errors for missing credentials and provider failures. Preserve record identity when updating supported fields. Require explicit targets for purges, cap URL purges to 30, and keep deletion/full-zone purge guarded. The interface does not cover Workers, Pages deployments, certificate management or all Cloudflare products.

## Non-negotiable boundaries

Zone ID and record ID define the target. Read, create/update, delete and cache invalidation have different effects. A successful Admin API response is not proof of worldwide DNS propagation or restored user traffic.

## Why this implementation

One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. Handlers pass explicit zone/record arguments to SDK resources. _record_to_dict normalizes optional fields/timestamps. This deliberately small source layout is appropriate to ten tools; no recorded alternative architecture decision was found. Adding a separate database or control plane would need a demonstrated use case.

## Current requirement debt

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

Classify a future statement as original requirement, later amendment, observed implementation, inferred rationale or proposed change. Preserve the distinction: source behavior does not silently repeal an original promise, and a plausible rationale is not a recorded decision.

## Supporting sources

- [README.md](../../README.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
