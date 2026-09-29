# Cloudflare DNS MCP: acceptance evidence

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | infrastructure operator managing an explicitly selected Cloudflare zone and DNS record. |
| **What?** | tests/test_server.py covers ten registered tool schemas, missing token, delete/full-purge denial, empty-purge target and optional DNS mapper fields. |
| **Where?** | tests/test_server.py. |
| **Why it exists?** | Cloudflare DNS MCP needs this document to choose a check that proves the changed behavior without claiming broader evidence. |
| **Why this approach?** | tests/test_server.py covers ten registered tool schemas, missing token, delete/full-purge denial, empty-purge target and optional DNS mapper fields. |
| **Why it matters?** | A registration or document check cannot prove live authentication, provider state or the installed user path. |

## Required proof by behavior

tests/test_server.py covers ten registered tool schemas, missing token, delete/full-purge denial, empty-purge target and optional DNS mapper fields. It does not exercise actual create/update retry behavior, DNS propagation or zone-setting SDK compatibility. For code changes run python -m unittest discover -s tests in a verified existing environment and add targeted fake-SDK tests; live DNS mutation is a separate approved acceptance path.

## Product acceptance baseline

Expose the ten implemented tools and return structured errors for missing credentials and provider failures. Preserve record identity when updating supported fields. Require explicit targets for purges, cap URL purges to 30, and keep deletion/full-zone purge guarded. The interface does not cover Workers, Pages deployments, certificate management or all Cloudflare products.

## Evidence custody

Inspected means source/test definitions were read. Locally verified means the named executable check actually ran and its result was observed. Live verified requires the deployed, installed or user-facing path. Historical checkmarks and CI configuration are not fresh results. Use the exact candidate, environment, test input class, observed result and limitations in a receipt. Read [AGENTS](AGENTS.md) for conditional AXI/crew custody; do not create a pipeline merely because this file exists.

## Supporting sources

- [tests/test_server.py](../../tests/test_server.py)

## Document checker setup

Use Python 3.10 or newer. In a virtual environment, install the pinned dependencies with `python -m pip install -r tools/requirements-workflow.txt` before running document checkers or fixtures. CommonMark parsing distinguishes rendered links and headings from examples; CI installs the same pins.

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
