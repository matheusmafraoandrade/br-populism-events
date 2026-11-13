"""Step 1: extract illiberal-action events from each source text with an LLM.

Output: data/events_raw.jsonl (one event per line, with provenance fields).
"""
import json
import os
import re
from datetime import datetime, timezone

import anthropic
from dotenv import load_dotenv

from common import DATA, SOURCES, load_codebook, load_config

SYSTEM_TEMPLATE = """You are a careful research assistant coding events for a dataset.
Follow the codebook below exactly.

{codebook}

Leader of interest: {leader}. Period of interest: {start} to {end}.

Return ONLY a JSON array (no prose, no code fences). Each element has the keys:
action, category, date, outcome, quote_action, quote_date, quote_outcome.
Quotes must be copied verbatim from the source text, in its original language.
Use null where the source does not support a field. If there are no events, return [].
"""


def parse_json(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)


def main():
    load_dotenv()
    cfg = load_config()
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    system = SYSTEM_TEMPLATE.format(
        codebook=load_codebook(), leader=cfg["leader"],
        start=cfg["period_start"], end=cfg["period_end"],
    )
    DATA.mkdir(exist_ok=True)
    out = DATA / "events_raw.jsonl"
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for path in sorted(SOURCES.glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            resp = client.messages.create(
                model=cfg["model"],
                max_tokens=4096,
                temperature=0,
                system=system,
                messages=[{"role": "user", "content": f"SOURCE TEXT:\n\n{text}"}],
            )
            try:
                events = parse_json(resp.content[0].text)
            except json.JSONDecodeError:
                print(f"[warn] could not parse JSON for {path.name}; skipped (check manually)")
                continue
            for ev in events:
                ev.update({
                    "source_file": path.name,
                    "model": cfg["model"],
                    "prompt_version": cfg["prompt_version"],
                    "extracted_at": datetime.now(timezone.utc).isoformat(),
                })
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
                n += 1
            print(f"{path.name}: {len(events)} events")
    print(f"Wrote {n} events to {out}")


if __name__ == "__main__":
    main()
