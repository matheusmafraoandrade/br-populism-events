"""Step 5 (optional): descriptive BRL/USD path around a few confirmed events.

Uses the Banco Central do Brasil SGS API, series 1 (USD/BRL, commercial selling rate, daily).
Descriptive only: no causal claims. Exchange rates respond to many things at once.
Output: figures/fx_events.png
"""
import io

import matplotlib.pyplot as plt
import pandas as pd
import requests

from common import DATA, FIGURES, load_config

SGS_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"
WINDOW_DAYS = 10
MAX_EVENTS = 4


def fetch_fx(start: str, end: str) -> pd.Series:
    fmt = lambda d: pd.Timestamp(d).strftime("%d/%m/%Y")
    r = requests.get(SGS_URL, params={"formato": "json", "dataInicial": fmt(start), "dataFinal": fmt(end)}, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = df["valor"].astype(float)
    return df.set_index("data")["valor"]


def main():
    cfg = load_config()
    ev = pd.read_csv(DATA / "events_clean.csv", parse_dates=["date_parsed"])
    ev = ev[(ev["verification"] == "confirmed") & (ev["date_precision"] == "day") & ~ev["flag_out_of_period"]]
    ev = ev.head(MAX_EVENTS)
    if ev.empty:
        print("No confirmed day-precision events; skipping.")
        return
    fx = fetch_fx(cfg["period_start"], cfg["period_end"])
    fig, axes = plt.subplots(len(ev), 1, figsize=(9, 2.6 * len(ev)), squeeze=False)
    for ax, (_, row) in zip(axes[:, 0], ev.iterrows()):
        d = row["date_parsed"]
        w = fx[d - pd.Timedelta(days=WINDOW_DAYS): d + pd.Timedelta(days=WINDOW_DAYS)]
        ax.plot(w.index, w.values)
        ax.axvline(d, color="red", ls="--", lw=1)
        ax.set_title(str(row["action"])[:90], fontsize=9)
        ax.set_ylabel("BRL/USD")
    fig.suptitle("BRL/USD around events (descriptive only, not causal)", fontsize=10)
    fig.tight_layout()
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / "fx_events.png", dpi=200)
    print("Saved figures/fx_events.png")


if __name__ == "__main__":
    main()
