"""Detect creature mentions in book descriptions and tags."""

import re
from typing import Dict, List

# Creature → list of aliases to match (word-boundary regex)
CREATURES: Dict[str, List[str]] = {
    "Dragon":   ["dragon", "dragons", "dragonfire", "wyrm", "wyvern", "drake"],
    "Witch":    ["witch", "witches", "witchcraft", "sorceress", "coven"],
    "Vampire":  ["vampire", "vampires", "vampiric", "vampyre"],
    "Elf":      ["elf", "elves", "elven", "elvish"],
    "Werewolf": ["werewolf", "werewolves", "lycanthrope", "lycan"],
    "Fae":      ["fae", "faerie", "faeries", "fairy", "fairies", "fey", "sidhe"],
    "Demon":    ["demon", "demons", "demonic"],
    "Ghost":    ["ghost", "ghosts", "specter", "spectre", "wraith", "phantom"],
    "Orc":      ["orc", "orcs", "orcish"],
    "Wizard":   ["wizard", "wizards", "sorcerer", "sorcerers", "mage", "mages"],
}

# Pre-compile one pattern per creature for speed
_PATTERNS = {
    creature: re.compile(
        r"\b(" + "|".join(re.escape(a) for a in aliases) + r")\b",
        re.IGNORECASE,
    )
    for creature, aliases in CREATURES.items()
}


def detect_creatures(book: dict) -> List[str]:
    """Return list of creature names mentioned in a book's description or tags."""
    # Build a single text blob: description + all tag names
    parts = [book.get("description") or ""]
    for tag_list in book.get("cached_tags", {}).values():
        parts.extend(t["tag"] for t in tag_list)
    text = " ".join(parts)

    return [creature for creature, pat in _PATTERNS.items() if pat.search(text)]
