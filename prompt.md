# Cloudflare DNS MCP - begin here

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation. |
| **Where?** | README.md, pyproject.toml, cf/server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to start the next task with the product’s actual purpose. |
| **Why this approach?** | Zone ID and record ID define the target. |
| **Why it matters?** | Zone ID and record ID define the target. |

## Product goal

Expose a small local MCP surface for zone discovery, DNS records, cache purge and page-rule inspection without dashboard navigation.

## Invariants

Zone ID and record ID define the target. Read, create/update, delete and cache invalidation have different effects. A successful Admin API response is not proof of worldwide DNS propagation or restored user traffic.

## Recover the current task

Source reconstruction: 2026-09-26; candidate `3b6b4f25fa52b1b4e7b9ec2c282503c3c7deed61` on `main`; source version `0.1.1`. This is a dated source observation, not a live-service or installed-version claim.

Initial 256099c on 2026-06-30 delivered ten tools; 86c9cbe bumped to 0.1.1 for ownership verification; July added guides/hermetic tests. Current main 3b6b4f2 is the September 16 CI-gate merge. That history does not prove a package is installed, service running or DNS change pending.

Use the latest user request as the task selector. This dossier is standing product context, not an instruction to repeat a completed documentation rollout. Recover applicable repository instructions, exact branch/candidate and dirty state, then bind the requested outcome and acceptance. If the only instruction is “read and begin,” finish this chain and perform a bounded read-only reconciliation of the current handoff and source; report the smallest next action, without inventing a product task or replaying historical external actions.

## Read chain

**Next: [INDEX.md](INDEX.md).** Read only task-relevant contracts before acting. Resolve relevant source contradictions before implementation; existing source documents remain canonical. Read deeper source when the selected task touches it.

## Task workflow

Select relevant skills from the active runtime's current catalog and instructions when the task requires them. This document does not activate a crew, pipeline, provider, or release.

## First unresolved work

The most material proposed work is mutation/retry safety and strict destructive-flag tests. Existing registration tests are insufficient proof of provider semantics. README packaging statements should be reconciled against a concrete built artifact when packaging is requested; do not infer distribution artifacts from prose. No real zone, pending change or owner-ranked backlog was read.

Before implementation, state the requested outcome, smallest useful change, evidence required and stop condition. Verify the actual result, update canonical sources and HANDOFFS, and leave knowledge events honest about freshness.
