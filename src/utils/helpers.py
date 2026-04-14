"""Common utility functions shared across the project."""

import json
from pathlib import Path
from typing import Union

import pandas as pd


def save_json(obj, path: Union[str, Path], indent: int = 2) -> None:
    """Serialize obj to JSON, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=indent, default=_json_default)


def _json_default(obj):
    """Handle types that json.dump can't serialize natively."""
    if isinstance(obj, float) and obj != obj:  # NaN
        return None
    if hasattr(obj, "item"):  # numpy scalar
        return obj.item()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def df_to_records(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame to a list of dicts, replacing NaN with None."""
    return json.loads(df.to_json(orient="records"))


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def slugify(text: str) -> str:
    """Lowercase, replace spaces with hyphens, strip non-alphanumeric."""
    import re
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))
