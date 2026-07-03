# Datos que Hablan: Bienestar Financiero de Jóvenes Profesionales en América Latina

**Capstone Project — Option B: Data Analyst Track**  
Cardiff University · Anahuac Mayab University · Funded by British Council Mexico 2026

---

## About This Project

This project analyses the *Encuesta de Bienestar Financiero 2025* — a survey of 500 young professionals aged 18–32 across six Latin American countries — to produce an executive report for the nonprofit **Futuro Digital LatAm**. The insights shape the design of a regional financial literacy programme.

---

## Project Structure

```
capstone-option-b/
├── data/
│   ├── latam_finanzas_2025.csv       # Raw survey data
│   └── latam_finanzas_clean.csv      # Cleaned dataset (output of Phase 2)
├── scripts/
│   ├── 01_explore.py                 # Phase 1 — Dataset exploration
│   ├── 02_clean.py                   # Phase 2 — Data cleaning
│   ├── 03_analyse.py                 # Phase 3 — Statistical analysis
│   ├── 04_visualise.py               # Phase 4 — Chart generation
│   ├── 05_interpret.md               # Phase 5 — Findings & interpretation
│   └── country_[name].py             # Country profiler scripts (x6)
├── charts/                           # 9 PNG visualisations
├── .claude/agents/
│   └── country-profiler.md           # Claude Code agent definition
├── Video_Demo/
│   └── Link_to_video.docx            # Link to the 5-minute demo video
├── analysis-report.md                # Executive report (Phase 6)
├── requirements.txt                  # Python dependencies
└── CLAUDE.md                         # Claude Code project instructions
```

---

## Setup Instructions

**Requirements:** Python 3.13+

1. Clone the repository:
   ```
   git clone https://github.com/Zetax-x/capstone-option-b_Emilio.git
   cd capstone-option-b_Emilio
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the scripts in order:
   ```
   python scripts/01_explore.py
   python scripts/02_clean.py
   python scripts/03_analyse.py
   python scripts/04_visualise.py
   ```

Charts will be saved to the `charts/` folder automatically.

---

## Analysis Phases

| Phase | Script | Output |
|-------|--------|--------|
| 1 — Explore | `01_explore.py` | Dataset overview, missing values, stats |
| 2 — Clean | `02_clean.py` | `data/latam_finanzas_clean.csv` |
| 2.5 — Agent | `.claude/agents/country-profiler.md` | `scripts/country_profiles.md` |
| 3 — Analyse | `03_analyse.py` | 6 statistical analyses |
| 4 — Visualise | `04_visualise.py` | 9 charts in `charts/` |
| 5 — Interpret | `05_interpret.md` | 10 findings with recommendations |
| 6 — Report | `analysis-report.md` | Executive report |

---

## Key Findings

1. The savings gap between age groups is **purely behavioural** — age does not predict income (r = -0.029)
2. Housing consumes **28.5%** of income on average, rising to **34.1%** in Argentina
3. AI tool usage correlates with financial satisfaction at **r = 0.57** (p < 0.0001)
4. All industry medians cluster within **$151** of each other — within-industry variance is the real income driver

---

*Encuesta de Bienestar Financiero 2025 · n = 500 · 6 countries · Ages 18–32*
