# 1. Plus achievements give a discount on the next month

- Status: Accepted
- Date: 2026-11-18

## Context

Saphi Plus is a monthly subscription (planned price: US$5/month). Gamification (streaks, tiered achievements) keeps users coming back, but rewards that only exist inside the app do not help retention of paying users. We want an incentive that ties good gardening habits to staying subscribed.

## Decision

1. Some achievement chains are **Plus achievements** (initially: Good neighbors, Sun reader, Weather-ready). They can only be earned with an active Plus subscription.
2. Each new tier of a Plus achievement earned during a billing month gives **20% off the next month**.
3. The discount is **applied automatically** at the next renewal. No codes, no manual redemption.
4. **One discount per month.** Discounts do not stack: earning two tiers in the same month still gives 20%.
5. Free-plan achievements keep their own rewards (e.g. a discount on a soil sensor at tier III), applied as a one-time coupon at checkout.
6. During the beta everything is free, so the discount is shown as an example and not charged.

## Alternatives considered

| Option | Why not |
|---|---|
| Points that convert to money | Hard to explain, creates a liability on the books, invites farming. |
| Stacking discounts (up to 100%) | A dedicated user could get Plus for free indefinitely; revenue becomes unpredictable. |
| Manual coupon codes | Friction; most users never redeem them. |
| No monetary reward | Loses the link between habits and retention. |

## Consequences

- Billing needs a "pending discount" per subscription, written by the achievements service and read once at renewal.
- Achievement progress must be tamper-resistant on the server (no client-reported tiers).
- Max cost per user is 20% of one month's price, so revenue stays predictable.
- The tier thresholds must be reachable through real use but not trivially gamed; review them after the first month of real data.
