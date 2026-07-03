# Capstone Project — Option B: Data Analyst

## Project Goal
Analyse the Encuesta de Bienestar Financiero 2025 survey data (500 respondents, 6 Latin American countries) and produce an executive report for Futuro Digital LatAm.

## Python Version
Python 3.13.0

## Key Libraries
- pandas — data manipulation
- matplotlib — charts
- seaborn — styled charts
- scipy — correlations and statistics

## Virtual Environment

**First-time setup (run this automatically if venv does not exist):**
```
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

Always use the project's virtual environment for all Python and pip commands:
- Python: `venv\Scripts\python.exe`
- Pip: `venv\Scripts\pip.exe`

Never use the global `python` or `pip` commands directly.

If the venv folder is missing when a session starts, create it and install dependencies from requirements.txt before doing anything else.

## Folder Structure
- `data/latam_finanzas_2025.csv` — raw data (do not modify)
- `data/latam_finanzas_clean.csv` — cleaned data (generated in Phase 2)
- `scripts/` — all Python scripts, named with phase prefix (e.g. 01_explore.py)
- `charts/` — all PNG charts, named clearly (e.g. 01_income_by_country.png)
- `.claude/agents/country-profiler.md` — custom agent definition
- `analysis-report.md` — final executive report

## Naming Conventions
- Scripts: `NN_description.py` (e.g. `01_explore.py`, `02_clean.py`)
- Charts: `NN_description.png` (e.g. `01_income_by_country.png`)
- Country scripts: `country_[name].py` (e.g. `country_mexico.py`)
