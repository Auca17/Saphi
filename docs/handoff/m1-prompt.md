# Handoff prompt — Milestone 1

Paste the block below into the coding agent (Devin via Orca) from the root of the `saphi` repository.

```text
You are the coding agent for Saphi. Work only in this repository.

1. Read, in this order: docs/BUILD.md (fully), docs/PRD.md, docs/adr/0001-plus-achievement-discounts.md, docs/adr/0002-paid-placement-only-in-shop-map.md, prototype/saphi-prototype.html (the visual and copy source of truth), saphi-startup/06-validation/experiment-design.md.

2. Implement ONLY "M1 — Waitlist with nursery QR codes + deploy" from docs/BUILD.md section 6. Do not start M2.

3. Rules:
   - Stack: Django 5.2 LTS monolith + HTMX, Python 3.12, uv, ruff, pytest-django. No React.
   - Code, comments, commits and docs in English. UI copy in Rioplatense Spanish, exactly as written in BUILD.md, wrapped for translation.
   - Create the branch feat/m1-waitlist from main. Never commit to main. Never force-push.
   - Test first: write the failing test for each validation rule and acceptance criterion in M1, then implement.
   - Conventional Commits, about 400 changed lines per commit max, tests and docs in the same commit as the behavior.
   - NEVER add "Co-Authored-By" or any AI attribution to commits or PRs.
   - Never commit secrets. Provide .env.example. Do not create external accounts (Render, Neon); write docs/DEPLOY.md so the founder can do it.
   - Do not edit prototype/, docs/PRD*.md, docs/adr/ or saphi-startup/.
   - If a product decision is missing, do not guess: list it as an open question in the PR.

4. Before opening the PR run and paste the output of:
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest

5. Open a PR titled "feat: M1 waitlist with nursery QR codes" with: what changed, how to test it locally and on a phone, screenshots at 375 px (light and dark), out of scope, open questions. Then stop and report the PR link.
```
