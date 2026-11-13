"""Step 4: timeline of confirmed events by category -> figures/timeline.png"""
import matplotlib.pyplot as plt
import pandas as pd

from common import DATA, FIGURES


def main():
    df = pd.read_csv(DATA / "events_clean.csv", parse_dates=["date_parsed"])
    df = df[(df["verification"] == "confirmed") & df["date_parsed"].notna() & ~df["flag_out_of_period"]]
    if df.empty:
        print("No confirmed, dated events to plot.")
        return
    cats = sorted(df["category"].unique())
    fig, ax = plt.subplots(figsize=(10, 0.8 * len(cats) + 1.5))
    for i, c in enumerate(cats):
        sub = df[df["category"] == c]
        ax.scatter(sub["date_parsed"], [i] * len(sub), s=60, alpha=0.8)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(cats)
    ax.set_title("Confirmed events by category (quotes verified against source)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / "timeline.png", dpi=200)
    print("Saved figures/timeline.png")


if __name__ == "__main__":
    main()
