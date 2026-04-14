"""Feature engineering on top of the loaded DataFrame."""

import pandas as pd


def add_era(df: pd.DataFrame) -> pd.DataFrame:
    """Bin release_year into broad literary eras."""
    bins = [-float("inf"), 0, 1800, 1950, 1980, 2000, 2010, float("inf")]
    labels = ["Ancient", "Pre-1800", "1800–1950", "1950–1980", "1980–2000", "2000–2010", "2010+"]
    df = df.copy()
    df["era"] = pd.cut(df["release_year"], bins=bins, labels=labels)
    return df


def add_popularity_tier(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a popularity tier based on ratings_count quartiles."""
    df = df.copy()
    df["popularity_tier"] = pd.qcut(
        df["ratings_count"].fillna(0),
        q=4,
        labels=["Niche", "Known", "Popular", "Beloved"],
    )
    return df


def add_normalized_rating(df: pd.DataFrame) -> pd.DataFrame:
    """Min-max normalize rating to [0, 1]."""
    df = df.copy()
    mn, mx = df["rating"].min(), df["rating"].max()
    df["rating_norm"] = (df["rating"] - mn) / (mx - mn)
    return df


def genre_counts(df: pd.DataFrame) -> pd.Series:
    """Count books per top_genre, sorted descending."""
    return df["top_genre"].value_counts().dropna()


def mood_counts(df: pd.DataFrame) -> pd.Series:
    return df["top_mood"].value_counts().dropna()


def ratings_by_era(df: pd.DataFrame) -> pd.DataFrame:
    """Mean rating and book count grouped by era."""
    return (
        df.groupby("era", observed=True)
        .agg(mean_rating=("rating", "mean"), count=("id", "count"))
        .reset_index()
    )


def top_authors(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Top N authors by number of books in the dataset."""
    return (
        df.groupby("author")
        .agg(book_count=("id", "count"), mean_rating=("rating", "mean"))
        .sort_values("book_count", ascending=False)
        .head(n)
        .reset_index()
    )
