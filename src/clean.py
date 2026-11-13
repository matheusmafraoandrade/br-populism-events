"""Step 3: clean and harmonize: parse dates, flag out-of-period rows, drop near-duplicates.

Output: data/events_clean.csv
"""
from difflib import SequenceMatcher

import pandas as pd

from common import DATA, load_config

CATEGORIES = {"judiciary", "media", "elections", "civil_service", "other_institutions"}
OUTCOMES = {"implemented", "blocked", "reversed", "ongoing", "unclear"}
RANK = {"confirmed": 2, "partial": 1, "unconfirmed": 0}


def parse_date(s):
    """Return (Timestamp or NaT, precision). Handles YYYY-MM-DD, YYYY-MM, YYYY."""
    if not isinstance(s, str) or not s.strip():
        return pd.NaT, None
    s = s.strip()
    for fmt, prec in (("%Y-%m-%d", "day"), ("%Y-%m", "month"), ("%Y", "year")):
        try:
            return pd.to_datetime(s, format=fmt), prec
        except ValueError:
            continue
    return pd.NaT, None


def similar(a, b, thr=0.8):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio() >= thr


def main():
    cfg = load_config()
    start, end = pd.Timestamp(cfg["period_start"]), pd.Timestamp(cfg["period_end"])
    df = pd.read_csv(DATA / "events_verified.csv")
    n0 = len(df)

    parsed = df["date"].apply(parse_date)
    df["date_parsed"] = [p[0] for p in parsed]
    df["date_precision"] = [p[1] for p in parsed]
    df["flag_no_date"] = df["date_parsed"].isna()
    df["flag_out_of_period"] = (~df["flag_no_date"]) & ((df["date_parsed"] < start) | (df["date_parsed"] > end))
    df["flag_bad_category"] = ~df["category"].isin(CATEGORIES)
    df["flag_bad_outcome"] = ~df["outcome"].isin(OUTCOMES)

    # Near-duplicates: same category, same (or both-missing) date, similar action text.
    # Keep the best-verified copy; record which sources it was seen in.
    df["_rank"] = df["verification"].map(RANK).fillna(0)
    df = df.sort_values("_rank", ascending=False).reset_index(drop=True)
    keep, seen_in = [], {}
    for i, row in df.iterrows():
        dup_of = None
        for j in keep:
            r = df.loc[j]
            same_date = (pd.isna(row["date_parsed"]) and pd.isna(r["date_parsed"])) or row["date_parsed"] == r["date_parsed"]
            if same_date and row["category"] == r["category"] and similar(row["action"], r["action"]):
                dup_of = j
                break
        if dup_of is None:
            keep.append(i)
            seen_in[i] = {row["source_file"]}
        else:
            seen_in[dup_of].add(row["source_file"])
    out = df.loc[keep].copy()
    out["sources_seen_in"] = [";".join(sorted(seen_in[i])) for i in out.index]
    out = out.drop(columns=["_rank"]).sort_values("date_parsed")
    out.to_csv(DATA / "events_clean.csv", index=False, encoding="utf-8")

    print(f"Events before: {n0} | after dedup: {len(out)} | duplicates removed: {n0 - len(out)}")
    print(out["verification"].value_counts().to_string())
    print("Flags:", out[[c for c in out.columns if c.startswith("flag_")]].sum().to_dict())


if __name__ == "__main__":
    main()
