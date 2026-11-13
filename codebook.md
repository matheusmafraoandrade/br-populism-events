# Codebook (v0.1)

## Unit of analysis

One **event** = one concrete, dated action (or attempted action) by the leader or the government under the leader's control that falls into one of the categories below. General statements, opinions and rhetoric without a concrete action are **not** events.

## Fields

| Field | Description |
|---|---|
| `action` | One-sentence description of what was done, in neutral language |
| `category` | One of the categories below |
| `date` | `YYYY-MM-DD`, or `YYYY-MM` / `YYYY` if only that precision is given in the source. `null` if not stated |
| `outcome` | One of: `implemented`, `blocked`, `reversed`, `ongoing`, `unclear` |
| `quote_action` | Verbatim quote from the source supporting the action |
| `quote_date` | Verbatim quote from the source supporting the date |
| `quote_outcome` | Verbatim quote supporting the outcome |

## Categories

- **judiciary**: actions toward courts or judges (appointments, packing, defiance of rulings, attacks on court independence, changes to court jurisdiction).
- **media**: actions toward press or journalists (legal or regulatory pressure, restriction of access, public funding or advertising changes tied to coverage).
- **elections**: actions toward electoral rules or bodies (challenges to the legitimacy of the electoral system, changes to rules, pressure on electoral authorities).
- **civil_service**: actions toward state employees or agencies (dismissals, politicized appointments, removal of heads of independent agencies).
- **other_institutions**: legislature, civil society, security forces or other constraints on executive power, when none of the above fits.

## Coding rules

1. Code only what the **source text** states. Do not use outside knowledge to fill in dates or outcomes.
2. Every field must be supported by a **verbatim** quote (same wording, same language as the source). If no quote supports it, set the field to `null`.
3. One event per concrete action. Do not merge separate actions into one event.
4. Use neutral, descriptive wording in `action`. No evaluative adjectives.
5. Attempted actions count; set `outcome` accordingly (`blocked`, `reversed`).
6. If unsure whether something qualifies, do **not** code it; log the case in `coding_decisions.md`.

## Changelog

- v0.1: initial draft.
