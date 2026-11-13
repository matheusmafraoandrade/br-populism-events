# br-populism-events

A small Python pipeline for identifying and coding illiberal actions associated with Jair Bolsonaro's government (2019–2022) from documentary sources and articles.

It is a miniature of an event-level data workflow: *AI-assisted coding → source verification → cleaning/harmonization → documentation*. The goal is not to make substantive claims about any politician, but to show a way of using LLMs for data construction.

## Pipeline

```
sources/*.txt ──► src/extract.py ──► data/events_raw.jsonl
                                          │
                                          ▼
                                   src/verify.py ──► data/events_verified.csv
                                          │
                                          ▼
                                    src/clean.py ──► data/events_clean.csv
```

1. **Codebook** (`codebook.md`): categories, definitions and coding rules. The LLM prompt is built from this file.
2. **Extraction** (`src/extract.py`): an LLM returns JSON events with `action`, `category`, `date`, `outcome` and a **verbatim quote** supporting each of action, date and outcome.
3. **Verification** (`src/verify.py`): checks whether extracted quotes appear in the original source text. Events are marked `confirmed`, `partial` or `unconfirmed` based on quote matching. This does not establish the substantive validity of an event.
4. **Cleaning** (`src/clean.py`): date parsing, out-of-period flags, missing sources, near-duplicate detection across sources.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with the following variable:

```env
GEMINI_API_KEY=your_api_key
```

## Usage

1. Edit `config.json` (leader, period of interest).
2. Put source texts in `sources/` (plain `.txt`) and log each one in `source_log.csv` (URL, access date, type).
3. Run:

```bash
python src/extract.py
python src/verify.py
python src/clean.py
```

## Documentation of how results are obtained

- Every raw event stores `source_file`, `model`, `prompt_version` and `extracted_at`.
- Coding decisions and ambiguities go to `coding_decisions.md`.
- Sources are logged in `source_log.csv`.

## Results

| Metric | Value |
|---|---|
| Sources used |5|
| Events extracted |5|
| Events classified as confirmed by quote matching |5|
| Duplicates removed |0|

## Limitations

- Small, non-representative set of sources; not a complete event history.
- Verbatim-quote matching catches fabricated quotes, but not every misinterpretation. A human read-through of a sample is still needed (see `coding_decisions.md`).
- Quotes from translated or paraphrased sources can fail exact matching; these are flagged, not silently dropped.
