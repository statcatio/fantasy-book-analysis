"""
Run the full data pipeline and write processed JSON files consumed by the
D3 visualization in analysis/index.html.

Usage:
    python scripts/process_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.data.loader import load_books
from src.features.extract import (
    add_era,
    add_normalized_rating,
    add_popularity_tier,
    genre_counts,
    mood_counts,
    ratings_by_era,
    top_authors,
)
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

    print("\nDone. Processed files written to data/processed/")


if __name__ == "__main__":
    main()
