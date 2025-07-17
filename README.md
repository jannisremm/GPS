# GPX Explorer

*A tiny Python utility to parse GPX tracks, derive simple statistics, and visualise them on an interactive map.*

---

## Why I built this

I have been recording a lot of GPX logs since moving to Hamburg, and wanted to create a simple project to visualise them and show some basic statistics, while learning matplotlib and pandas.

The result:

*  **Converts GPX to a DataFrame** (`longitude`, `latitude`, `height`, `speed`, `hdop`, `time`).
*  **Merges dozens of tracks** into one CSV for aggregate analysis.
*  **Picks a random track** highlights one journey on the map and shows details in the other plots.
*  **Visualise speed, altitude & GPS accuracy** in a single Matplotlib figure.

---

## Demo

![example figure](example_output.png)

*(Tracks around Hamburg - red line highlights the randomly‑chosen ride; colour scale shows speed; annotations mark top speed & highest point.)*

---

## Installation

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt                      # or see minimal deps below
```

### Minimal requirements

```bash
pip install pandas matplotlib cartopy gpxpy
```

*Python ≥ 3.10 is recommended.*

---

## Quick Start

```bash
# 1. Put your .gpx files into the tracks/ directory
# 2. Run this command in the terminal from the main directory
python gpx_explorer.py

# Optional: combine all tracks into a CSV cache
python gpx_explorer.py --combine --out combined_gpx_tracks.csv
```

---


## Roadmap

* Clean up graphs:
    * Make sure annotations stay within borders of graph, and don't overlap points or each other
    * Add Values to Top Speed and Max Height annotations
    * Make sure gridlines have regular equal intervals
* Identify stops on the individual graph
* Turn the script into a CLI:
    * Add options for how many stats to show
    *allow users to highlight certain track
* Elevation gain / loss, grade, movement time, distance covered stats.
* Use information from stops to cluster tracks 
* Create Unit tests
* Package & publish on PyPI (maybe)

---