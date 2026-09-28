# Cloudflare DNS MCP: evidence and unresolved claims

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | The most material proposed work is mutation/retry safety and strict destructive-flag tests. |
| **Where?** | README.md, pyproject.toml, cf/server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to show what is observed, what remains unknown and what decision follows. |
| **Why this approach?** | The most material proposed work is mutation/retry safety and strict destructive-flag tests. |
| **Why it matters?** | These limits keep the next task honest and bounded. |

## Reconstruction finding

Source reconstruction: 2026-09-26; candidate `3b6b4f25fa52b1b4e7b9ec2c282503c3c7deed61` on `main`; source version `0.1.1`. This is a dated source observation, not a live-service or installed-version claim.

The earlier workflow-adoption completion has been superseded by the user’s request for substantive product reconstruction. The enduring product outcome is: Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation.

## Established from sources

One cf/server.py module owns FastMCP registration, a lazy cached Cloudflare SDK client, _call retry wrapper and DNS mapper. Handlers pass explicit zone/record arguments to SDK resources. _record_to_dict normalizes optional fields/timestamps. This deliberately small source layout is appropriate to ten tools; no recorded alternative architecture decision was found. Adding a separate database or control plane would need a demonstrated use case.

Initial 256099c on 2026-06-30 delivered ten tools; 86c9cbe bumped to 0.1.1 for ownership verification; July added guides/hermetic tests. Current main 3b6b4f2 is the September 16 CI-gate merge. That history does not prove a package is installed, service running or DNS change pending.

## Unresolved product claims

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

## Evidence limits and value

This reconstruction makes the next task’s interfaces, boundaries and prior intent recoverable. It does not establish new customer value, provider success or a deployed fix. No current product build, account request, browser launch, private corpus read, publish or release was performed. Structural document validation and source-grounded scenario read-through are recorded separately from product acceptance. [TESTING](TESTING.md) identifies the additional proof a future implementation needs.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [cf/server.py](../../cf/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
