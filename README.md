# Fantasy Book Explorer

An interactive data analysis of **1,000 fantasy books** — exploring ratings, genres, moods, authors, and how the genre has evolved across literary eras.

**[View the interactive visualization →](analysis/index.html)**

![Overview showing rating by era, genre distribution, and author rankings](https://via.placeholder.com/900x400/0f0f1a/f5a623?text=Fantasy+Book+Explorer)

---

## What's inside

| View | What you'll find |
|------|-----------------|
| **Overview** | Key stats + average rating by literary era |
| **Year × Rating** | Scatter plot of 982 books colored by genre, mood, or series status |
| **Genres** | Top 15 genres by book count |
| **Moods** | Emotional tone distribution (donut chart) |
| **Authors** | Most prolific authors, colored by mean rating |

---

## Dataset

`data/raw/fantasy_books.json` — 1,000 books with:

- `title`, `release_year`, `pages`
- `rating`, `ratings_count`
- `cached_tags` — Genre, Mood, Content Warning, and freeform Tag taxonomy
- `contributions` — author(s)
- `book_series` — series name and position

Year range: **800 BC – 2025**

---

## Project structure

```
fantasy-book-explorer/
├── data/
│   ├── raw/                  # Original dataset (never modified)
│   │   └── fantasy_books.json
│   └── processed/            # Output of scripts/process_data.py
│       ├── scatter.json
│       ├── genres.json
│       ├── moods.json
│       ├── ratings_by_era.json
│       └── top_authors.json
├── src/
│   ├── data/
│   │   └── loader.py         # Load raw JSON → flat DataFrame
│   ├── features/
│   │   └── extract.py        # Era binning, popularity tiers, aggregations
│   └── utils/
│       └── helpers.py        # JSON serialization, slugify, etc.
├── scripts/
│   └── process_data.py       # End-to-end pipeline → data/processed/
├── analysis/
│   └── index.html            # D3.js interactive dashboard (self-contained)
├── requirements.txt
└── environment.yml
```

---

## Quickstart

### 1. Set up the environment

**With conda (recommended):**
```bash
conda env create -f environment.yml
conda activate fantasy-book-explorer
```

**With pip:**
```bash
pip install -r requirements.txt
```

### 2. Run the data pipeline

```bash
python scripts/process_data.py
```

This reads `data/raw/fantasy_books.json` and writes five JSON files to `data/processed/`.

### 3. Open the visualization

```bash
# From the repo root — any local server works
python -m http.server 8000
# then open http://localhost:8000/analysis/
```

> The HTML file loads data from `../data/processed/` via relative paths, so a local server is needed (no `file://` protocol).

---

## Key findings

- **2010+ books** have the highest average reader rating in the dataset, suggesting recency bias or genuine quality growth in the genre.
- **Fantasy** and **Fiction** dominate the genre tags; **Adventure** and **Young Adult** follow closely.
- **Adventurous** and **Emotional** are the most common mood tags — fantasy readers skew toward plot-driven, emotionally resonant stories.
- Series books outnumber standalones and tend to accumulate more ratings, consistent with reader investment in multi-book arcs.

---

## Tech stack

| Layer | Tool |
|-------|------|
| Data processing | Python · pandas · numpy |
| Visualization | D3.js v7 (CDN, no build step) |
| Environment | conda / pip |

---

## Contributing

Pull requests welcome. If you extend the analysis, please:
1. Add new processing logic to `src/` and export new JSON from `scripts/process_data.py`
2. Add a new view or chart to `analysis/index.html`
3. Update this README with your findings

---

## License

MIT
