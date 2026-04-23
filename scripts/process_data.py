"""
Run the full data pipeline and write processed JSON files consumed by the
D3 visualization in analysis/index.html.

Usage:
    python scripts/process_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.data.loader import load_books, load_raw
from src.features.extract import (
    add_era,
    add_normalized_rating,
    add_popularity_tier,
    genre_counts,
    mood_counts,
    ratings_by_era,
    top_authors,
)
from src.features.creatures import CREATURES, detect_creatures
from src.utils.helpers import df_to_records, save_json

OUT = Path("data/processed")


def main():
    print("Loading books...")
    df = load_books()
    df = add_era(df)
    df = add_popularity_tier(df)
    df = add_normalized_rating(df)

    # Filter out books with missing core fields for the scatter plot
    scatter_df = df.dropna(subset=["release_year", "rating", "ratings_count"]).copy()
    # Exclude ancient outliers for readability (keep 1800+)
    scatter_df = scatter_df[scatter_df["release_year"] >= 1800]

    # 1. Scatter data: year vs rating, sized by popularity
    save_json(df_to_records(scatter_df[[
        "id", "title", "author", "release_year", "rating",
        "ratings_count", "top_genre", "top_mood", "is_series", "pages", "era"
    ]]), OUT / "scatter.json")
    print(f"  scatter.json  — {len(scatter_df)} books")

    # 2. Genre distribution
    gc = genre_counts(df).reset_index()
    gc.columns = ["genre", "count"]
    save_json(df_to_records(gc.head(15)), OUT / "genres.json")
    print(f"  genres.json   — {len(gc)} genres")

    # 3. Mood distribution
    mc = mood_counts(df).reset_index()
    mc.columns = ["mood", "count"]
    save_json(df_to_records(mc.head(12)), OUT / "moods.json")
    print(f"  moods.json    — {len(mc)} moods")

    # 4. Ratings by era
    rbe = ratings_by_era(scatter_df)
    save_json(df_to_records(rbe), OUT / "ratings_by_era.json")
    print(f"  ratings_by_era.json — {len(rbe)} eras")

    # 5. Top authors
    ta = top_authors(df, n=20)
    save_json(df_to_records(ta), OUT / "top_authors.json")
    print(f"  top_authors.json — {len(ta)} authors")

    # 6. Creature timeline
    raw_books = load_raw()
    creature_timeline = _build_creature_timeline(raw_books, df)
    save_json(creature_timeline, OUT / "creature_timeline.json")
    print(f"  creature_timeline.json — {len(creature_timeline)} decades")

    print("\nDone. Processed files written to data/processed/")


def _build_creature_timeline(raw_books: list, df) -> list:
    """
    For each decade (1800–2020), compute what % of books published that decade
    mention each creature. Returns a list of dicts, one per decade.
    """
    import math

    # Map book id → release_year from the flat DataFrame
    year_map = df.set_index("id")["release_year"].dropna().to_dict()

    # Bucket each raw book into a decade and record creature hits
    decade_totals: dict = {}   # decade → total book count
    decade_hits: dict = {}     # decade → {creature → count}

    for book in raw_books:
        year = year_map.get(book["id"])
        if not year or math.isnan(float(year)) or year < 1800 or year > 2025:
            continue
        decade = int(year // 10) * 10
        decade_totals[decade] = decade_totals.get(decade, 0) + 1

        mentioned = detect_creatures(book)
        if decade not in decade_hits:
            decade_hits[decade] = {c: 0 for c in CREATURES}
        for c in mentioned:
            decade_hits[decade][c] += 1

    rows = []
    for decade in sorted(decade_totals):
        total = decade_totals[decade]
        row = {"decade": decade, "total": total}
        hits = decade_hits.get(decade, {})
        for creature in CREATURES:
            count = hits.get(creature, 0)
            row[creature] = round(count / total * 100, 1)
            row[f"{creature}_count"] = count
        rows.append(row)
    return rows


if __name__ == "__main__":
    main()
