"""Load and parse the raw fantasy books JSON into a flat DataFrame."""

import json
from pathlib import Path
from typing import Optional

import pandas as pd

RAW_PATH = Path(__file__).parents[2] / "data" / "raw" / "fantasy_books.json"


def load_raw(path: Path = RAW_PATH) -> list[dict]:
    with open(path) as f:
        return json.load(f)["data"]["books"]


def load_books(path: Path = RAW_PATH) -> pd.DataFrame:
    """Return a cleaned, flat DataFrame with one row per book."""
    books = load_raw(path)
    rows = []
    for b in books:
        rows.append({
            "id": b["id"],
            "title": b["title"],
            "release_year": b.get("release_year"),
            "pages": b.get("pages"),
            "rating": b.get("rating"),
            "ratings_count": b.get("ratings_count"),
            "author": _primary_author(b),
            "top_genre": _top_tag(b, "Genre"),
            "top_mood": _top_tag(b, "Mood"),
            "series_name": _series_name(b),
            "is_series": bool(b.get("book_series")),
            "genres": _all_tags(b, "Genre"),
            "moods": _all_tags(b, "Mood"),
        })
    return pd.DataFrame(rows)


# --- helpers -----------------------------------------------------------------

def _primary_author(book: dict) -> Optional[str]:
    contribs = book.get("contributions", [])
    if contribs:
        return contribs[0]["author"]["name"]
    return None


def _top_tag(book: dict, category: str) -> Optional[str]:
    tags = book.get("cached_tags", {}).get(category, [])
    if tags:
        return max(tags, key=lambda t: t["count"])["tag"]
    return None


def _all_tags(book: dict, category: str) -> list:
    return [t["tag"] for t in book.get("cached_tags", {}).get(category, [])]


def _series_name(book: dict) -> Optional[str]:
    series = book.get("book_series", [])
    if series:
        return series[0]["series"]["name"]
    return None
