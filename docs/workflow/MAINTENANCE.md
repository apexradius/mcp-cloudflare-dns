# Cloudflare DNS MCP: operation and recovery

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Entrypoint cf.server:main. |
| **Where?** | README.md. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to recover safely from the actual failure modes rather than repeat old operations. |
| **Why this approach?** | Entrypoint cf.server:main. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Runtime and recovery

Entrypoint cf.server:main. Resolve CF_API_TOKEN first, falling back to CLOUDFLARE_API_TOKEN. The SDK client is cached, so credential changes do not automatically prove the running process picked them up. No runtime was started here. Recovery for DNS uses the exact saved record state; cache purge cannot be undone by restoring a local file.

## Prioritized uncertainty

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

## Closeout

Verify the requested result at the correct layer, reconcile the owning manual/interface and update [HANDOFFS](HANDOFFS.md). Record a [knowledge event](REFERENCES.md) for material source/decision/freshness changes. Do not run package publishing, provider writes, private index sync or browser automation just to refresh a document.

## Supporting sources

- [README.md](../../README.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
