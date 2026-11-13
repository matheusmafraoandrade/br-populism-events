"""Step 2: verify that every quote appears verbatim in its source text.

Status per event:
  confirmed   - all non-null quotes found in the source
  partial     - some quotes found, some not
  unconfirmed - no quote found (or no quotes at all)
Output: data/events_verified.csv
"""
import json

import pandas as pd

from common import DATA, SOURCES, normalize

QUOTE_FIELDS = ["quote_action", "quote_date", "quote_outcome"]


def main():
    events = [json.loads(l) for l in (DATA / "events_raw.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    cache = {}
    rows = []
    for ev in events:
        src = ev["source_file"]
        if src not in cache:
            cache[src] = normalize((SOURCES / src).read_text(encoding="utf-8"))
        found, total = 0, 0
        for q in QUOTE_FIELDS:
            val = ev.get(q)
            if val:
                total += 1
                ok = normalize(val) in cache[src]
                ev[f"{q}_found"] = ok
                found += ok
            else:
                ev[f"{q}_found"] = None
        if total == 0 or found == 0:
            ev["verification"] = "unconfirmed"
        elif found == total:
            ev["verification"] = "confirmed"
        else:
            ev["verification"] = "partial"
        rows.append(ev)
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "events_verified.csv", index=False, encoding="utf-8")
    print(df["verification"].value_counts().to_string())


if __name__ == "__main__":
    main()
