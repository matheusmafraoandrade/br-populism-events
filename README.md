# br-illiberal-events

A small, fully documented pipeline that codes **illiberal actions by a populist leader in government** (case: Brazil) from source texts, verifies every coded event against the original document, cleans the resulting dataset and visualizes it.

It is a miniature of an event-level data workflow: *AI-assisted coding → source verification → cleaning/harmonization → documentation → figures*. The goal is not to make substantive claims about any politician, but to show a careful, auditable way of using LLMs for data construction.

## Pipeline

```
sources/*.txt ──► src/extract.py ──► data/events_raw.jsonl
                                          │
                                          ▼
                                   src/verify.py ──► data/events_verified.csv
                                          │
                                          ▼
                                    src/clean.py ──► data/events_clean.csv
                                          │
                         ┌────────────────┴────────────────┐
                         ▼                                 ▼
                    src/plot.py                        src/fx.py (optional)
              figures/timeline.png            figures/fx_events.png
```

1. **Codebook** (`codebook.md`): categories, definitions and coding rules. The LLM prompt is built from this file.
2. **Extraction** (`src/extract.py`): an LLM returns JSON events with `action`, `category`, `date`, `outcome` and a **verbatim quote** supporting each of action, date and outcome.
3. **Verification** (`src/verify.py`): checks programmatically that each quote appears in the source text. Events are marked `confirmed`, `partial` or `unconfirmed`. Nothing is trusted just because the model said it.
4. **Cleaning** (`src/clean.py`): date parsing, out-of-period flags, missing sources, near-duplicate detection across sources.
5. **Figures** (`src/plot.py`, `src/fx.py`): timeline of confirmed events by category; optional descriptive BRL/USD chart (Banco Central SGS API) around events. **Descriptive only, no causal claims.**

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GEMINI_API_KEY from Google AI Studio
```

## Usage

1. Edit `config.json` (leader, period of interest).
2. Put source texts in `sources/` (plain `.txt`) and log each one in `source_log.csv` (URL, access date, type).
3. Run:

```bash
python src/extract.py
python src/verify.py
python src/clean.py
python src/plot.py
python src/fx.py   # optional
```

## Documentation of how results are obtained

- Every raw event stores `source_file`, `model`, `prompt_version` and `extracted_at`.
- Coding decisions and ambiguities go to `coding_decisions.md`.
- Sources are logged in `source_log.csv`.

## Results (fill in after running)

| Metric | Value |
|---|---|
| Sources used | |
| Events extracted | |
| Confirmed / partial / unconfirmed | |
| Duplicates removed | |

## Limitations

- Small, non-representative set of sources; not a complete event history.
- Verbatim-quote matching catches fabricated quotes, but not every misinterpretation. A human read-through of a sample is still needed (see `coding_decisions.md`).
- Quotes from translated or paraphrased sources can fail exact matching; these are flagged, not silently dropped.
- Exchange-rate movements around events are descriptive and confounded by many other factors.
