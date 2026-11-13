"""Shared helpers: paths, config, codebook loading."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
DATA = ROOT / "data"
FIGURES = ROOT / "figures"


def load_config() -> dict:
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def load_codebook() -> str:
    return (ROOT / "codebook.md").read_text(encoding="utf-8")


def normalize(text: str) -> str:
    """Normalize text for quote matching: unify quotes/dashes, collapse whitespace, lowercase."""
    repl = {"‘": "'", "’": "'", "“": '"', "”": '"',
            "–": "-", "—": "-", " ": " "}
    for a, b in repl.items():
        text = text.replace(a, b)
    return " ".join(text.split()).lower()
