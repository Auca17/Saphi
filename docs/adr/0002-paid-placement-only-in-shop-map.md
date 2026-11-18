# 2. Paid placement only affects the shop map, never plant advice

- Status: Accepted
- Date: 2026-11-18

## Context

Saphi is free for users. The planned revenue source (after the MVP) is a map of nurseries and flower shops in Mendoza, where shops pay to be recommended. Saphi's core promise is honest guidance: plant recommendations, warnings, and the AI advisor must be trustworthy. If money could change what Saphi recommends, users would stop trusting it.

## Decision

1. Shops can pay to **rank higher in the shop map**, and only **when the user searches for a plant type that shop sells**. Distance to the user is always part of the ranking.
2. Paid results are labeled **"Destacado"**.
3. Payment **never** changes which plants Saphi recommends, the rule engine's warnings, the advisor's answers, the catalog, or "Sow this month".
4. The shop list is curated by hand for the MVP (shops visited in person, with their consent) and stored long-term. No scraping of Google Maps (its terms forbid it).
5. The app stays free for users; Saphi Plus (ADR 0001) remains a later option.

## Alternatives considered

| Option | Why not |
|---|---|
| Sponsored plant recommendations | Breaks the honest-guidance principle; users would doubt every suggestion. |
| Commission per sale inside the app | Requires payments, stock, and returns handling: a different business. |
| Ads | Low revenue at small scale and conflicts with "no data exploitation". |

## Consequences

- The shop map needs a ranking function with an explicit, auditable "paid boost" term, separate from the plant recommendation code.
- Advisor and rule-engine code must not read shop or payment data.
- The shop map is a post-MVP feature; the MVP focuses on the user app.
