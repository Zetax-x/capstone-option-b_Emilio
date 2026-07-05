---
name: interpret
description: Writes a structured policy-facing interpretation of one statistical finding from the LatAm financial wellness dataset, with labeled sections, statistical validation, a reconciliation note when needed, a conceptual label, cross-finding correlations with auto-generated charts, discrepancy tracking, and a general conclusion after the last finding
---

**Scope:** This skill applies to all 18 interpretable items from the LatAm pipeline:
- **Findings 1–14** — from `scripts/03_analyse.py`, visualised in `charts/01–12`
- **Correlation Charts 13–14** — from `scripts/06_correlations.py` (cross-finding country-level correlations)
- **Advanced Analysis 15–18** — from `scripts/07_advanced.py` (negative savers, OLS, clustering, FDR)

If the item is a **Correlation Chart (13–14)** or an **Advanced Analysis section (15–18)**, start with **Step 0** before proceeding to Steps 1–4. For Findings 1–14, skip Step 0.

Step 4 (General Conclusion) runs only when ALL 18 items have been interpreted — not just the 14 findings.

---

## Step 0 — Extended interpretation for Charts 13–18

Use this step **only** for items from `06_correlations.py` or `07_advanced.py`.

### Correlation Charts (06_correlations.py)

**Chart 13 — Carga de vivienda vs. ahorro promedio por país (`13_vivienda_vs_ahorro.png`)**
- What it shows: a scatter plot with 6 country-level points. Each point is a country's average housing burden (% of income) on the x-axis vs. average monthly savings (USD) on the y-axis. Point size = median income. Includes a Pearson r and p-value.
- How to interpret: describe the direction of the relationship (if housing burden is higher, do people save less or more?), state the r and p-value, then flag the key limitation: with only 6 country-level points, the statistical power is very low (you need r > 0.81 to reach p < 0.05). Treat it as a descriptive pattern, not a causal claim.
- Link to findings: cross-reference Hallazgo 6 (housing burden by country) and Hallazgo 2 (savings gap). Explain which countries are the outliers and what the programme implication is.

**Chart 14 — Uso de IA vs. satisfacción financiera por país (`14_ia_vs_satisfaccion.png`)**
- What it shows: same scatter format, with country-level average AI usage (hrs/week) on the x-axis vs. average financial satisfaction (1–5 scale). Point size = median income.
- How to interpret: state whether the country-level pattern matches the individual-level finding (Hallazgo 5: r = 0.571 at individual level). Note whether countries with higher AI usage tend to have higher satisfaction, and flag the same n=6 limitation.
- Link to findings: cross-reference Hallazgo 5 and Hallazgo 10. If the pattern at country level contradicts the individual-level finding, flag it as a tension (Step 3 discrepancy protocol).

### Advanced Analysis (07_advanced.py)

**Chart 15 — Perfil de ahorradores negativos (`15_negative_savers_profile.png`)**
- What it shows: a comparison of key financial metrics between the 74 participants with negative monthly savings (spend more than they earn) vs. the 426 with positive savings.
- How to interpret: identify which metrics differ most between groups (credit card ownership, debt, housing burden, satisfaction). Emphasise that this subgroup has similar income to the rest — the problem is not earnings but the combination of financial instruments and structural costs that eliminate their margin.
- Link to findings: cross-reference Hallazgo 12 (debt vs savings), Hallazgo 6 (housing burden), Hallazgo 4 (credit card usage). This subgroup is the extreme case of the patterns found elsewhere.

**Chart 16 — Coeficientes OLS (`16_ols_coefficients.png`)**
- What it shows: a horizontal bar chart of standardised regression coefficients for 6 predictors (age, income, AI usage, credit card, debt, savings account) from a multivariate OLS model. Bars with confidence intervals crossing zero are non-significant.
- How to interpret: R² = 0.268 means the 6 variables together explain 26.8% of the variation in monthly savings (think of it like: if you had to guess someone's savings using only these 6 facts about them, you'd be 26.8% more accurate than guessing the average for everyone). The two significant predictors are age (strongest) and income. The four non-significant ones — AI, credit card, debt, savings account — have confidence intervals that include zero, meaning their apparent effect could be zero.
- Key conclusion to draw: when age and income are controlled for, no financial instrument has an independent effect. This validates Hallazgo 11 from a completely different angle.
- Link to findings: Hallazgos 2, 4, 5, 11, 12.

**Chart 17 — Radar de clusters (`17_user_clusters.png`)**
- What it shows: a radar (spider) chart with three overlapping polygons, one per cluster (En Riesgo, En Camino, Avanzado). Each axis is a normalised financial variable (income, savings, satisfaction, AI usage, debt rate).
- How to interpret: identify which axis each cluster "dominates" and what that means for programme targeting. "Avanzado" should show clear dominance on income, savings, and AI. "En Camino" should show 100% debt. "En Riesgo" should show flat low values everywhere.
- Key conclusion to draw: the three clusters suggest three different entry points for programme modules — not a single curriculum. Describe who goes into each cluster and what intervention would most help them.
- Link to findings: cross-references all 14 prior findings as validation; the cluster profiles summarise the findings into actionable audience segments.

**Chart 18 — Corrección FDR Benjamini-Hochberg (`18_fdr_bh_correction.png`)**
- What it shows: the 5 formal Pearson tests ranked by p-value, with BH-adjusted significance thresholds overlaid. Tests above the threshold are non-significant; those below survive FDR correction.
- How to interpret: explain in plain language that when you run many statistical tests, some will appear significant by luck alone. The BH correction adjusts for this. The two significant findings (IA vs satisfaction, IA vs income) survive — this means they are robust, not artifacts of running many tests. The three null findings (F7, F11, F12) were already non-significant and the correction does not change their status.
- Key conclusion to draw: the project's significant conclusions are statistically solid. There are no borderline findings in the "grey zone" that the correction might flip.
- Link to findings: Hallazgos 5, 7, 10, 11, 12.

After completing Step 0 for Charts 13–18, continue to Steps 1–3 using the information above as the basis for **Los datos**, **¿Por qué importa?**, **Recomendación**, and **Mecanismo** sections. Adapt the section headers to reference the chart number rather than a finding number (e.g., "**Gráfica 13: Carga de Vivienda vs. Ahorro por País**").

---

When given a statistical finding from the Encuesta de Bienestar Financiero 2025,
do the following in order:

## Step 1 — Write the interpretation

Write the finding in Spanish using these four labeled sections:

**Hallazgo [N]: [Finding title]**

**Los datos:** One paragraph stating what the data shows. Include all relevant numbers
(means, medians, percentages, counts). If a key assertion implies that two groups are
"similar" or that a variable "does not explain" a pattern, include or cite the Pearson r
and p-value that supports it — or explicitly mark the assertion as *"no verificado
estadísticamente"* if the test has not been run.

**¿Por qué importa?:** One paragraph explaining the consequence for Futuro Digital LatAm's
financial literacy programme. Name the specific audience group, country, or market condition
most affected. Do not repeat the numbers — interpret them. This section should answer
"so what?" for a board member who will not read the data tables.

**Recomendación:** One paragraph with one concrete, specific programme action backed
directly by this finding. Avoid generic advice ("educate participants about X"). Name
the module, the target audience, the mechanism, and the measurable outcome where possible.

**Nota de reconciliación (only if needed):** If any number in this finding could appear
to contradict a statistic from a previous finding when read in isolation, add this section.
Explain in plain language why both numbers are correct and how the mechanism works
(e.g. different subgroups, median vs. mean, within-group vs. between-group variation).
If no potential confusion exists, omit this section entirely — do not write it as
"N/A" or "no aplica".

**Mecanismo:** One bold line naming the underlying dynamic in 4–8 words — not the
correlation, but the mechanism. Examples: **"Brecha de hábito, no de ingreso"**,
**"Involucramiento activo como predictor de resultados"**, **"Presión estructural
independiente del comportamiento individual"**. This label should be memorable enough
that a board member can repeat it in a meeting.

**Fuente:** Cite the specific statistics used, with script reference (e.g.
`scripts/03_analyse.py`).

## Step 2 — Check for correlations with previous findings

Review all findings interpreted so far in this session (from context or from
scripts/country_profiles.md and scripts/03_analyse.py results).

Ask: does this new finding share an underlying variable or pattern with any previous finding?
Examples of meaningful correlations to look for:
- Two findings that both vary by country in the same direction
- A variable that appears in multiple findings (e.g. income, AI usage, age)
- A finding where the cause might be explained by another finding's result

If NO meaningful correlation is found: state "No se encontró correlación significativa con hallazgos anteriores." and stop.

If a correlation IS found:

1. Describe it in one sentence in Spanish: which two findings are related and how.

2. Write a Python script using data/latam_finanzas_clean.csv to visualise the correlation.
   - Determine N = number of existing PNG files in charts/ (use os.listdir or glob)
   - Name the file: charts/{N+1:02d}_{variable1}_vs_{variable2}.png
     (use short snake_case names derived from the column names, e.g. ingreso_vs_satisfaccion)
   - Chart type: scatter plot with regression line, or dual-axis bar chart if comparing group averages
   - Style: match the professional palette used in Phase 4 (avoid default matplotlib colors)
   - Include: clear title in Spanish, labelled axes, source note
     "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
   - Print the Pearson r and p-value on the chart as an annotation

3. Save and run the script. Confirm the chart was saved with its full filename.

## Step 3 — Check for discrepancies

This step catches only discrepancies that were NOT already resolved by a "Nota de
reconciliación" in Step 1. A reconciliation note handles apparent contradictions that
have a clear mechanical explanation. Step 3 handles tensions where both interpretations
are valid but the data pulls in different directions.

Compare this finding's interpretation against all previous findings and the raw
statistics from Phase 3 (scripts/03_analyse.py output). Look for:
- A recommendation that conflicts with a recommendation from a previous finding
- A statistic cited in the interpretation that does not match the Phase 3 output
- A generalisation that the data only partially supports (e.g. claiming "all countries"
  when only 3 of 6 show the pattern)
- Two correct findings that imply opposite programme priorities for the same audience

If NO discrepancy is found: state "Sin discrepancias detectadas." and move to Step 4.

If a discrepancy IS found, determine its cause:

**Case A — Misinterpretation (the data is fine but the text is wrong):**
- Clearly state what was wrong and why
- Rewrite only the affected section(s) from Step 1 to correct the error
- Mark the corrected block with: ⚠️ *Corrección aplicada: [one-line reason]*

**Case B — Real tension in the data (both findings and interpretations are correct):**
- State the tension in one sentence in Spanish
- Explain briefly why the two findings can coexist (e.g. different subgroups, confounding variable)
- Provide one concrete suggestion for how the programme could address or investigate the tension
- Mark the block with: 💡 *Discrepancia real: [one-line description] — Sugerencia: [one-line suggestion]*

## Step 4 — General conclusion (only when all 18 items are done)

This step runs ONLY when all 18 interpretable items have been processed in this session:
Findings 1–14 (from 03_analyse.py), Charts 13–14 (from 06_correlations.py), and Advanced
Analysis sections 15–18 (from 07_advanced.py). Do not run this step after item 14 if
items 13–18 from the correlation and advanced scripts have not yet been interpreted.
Determine this by checking that no items from the full set of 18 are missing from the
sequence seen so far in context.

Write the conclusion in Spanish under the header **Conclusión General**, using the
following structure:

**2–4 numbered higher-order insights, each with a bold title.**

Each insight must:
- Synthesise 2 or more findings into a single narrative claim — not summarise them individually
- Cite the specific finding numbers it draws from (e.g. "Hallazgos 2, 7 y 8")
- If a correlation confirmed in Step 2 is relevant to this insight, reference it and
  the chart generated (e.g. "confirmado en charts/06_ahorro_vs_edad.png")
- If a real discrepancy flagged in Step 3 is relevant, integrate it naturally as a
  caveat or open question within the insight — do not isolate it in a separate paragraph
- End with one concrete programme implication that follows directly from the insight

After the numbered insights, add a single closing paragraph (2–3 sentences) titled
**Recomendación prioritaria** that states the one action that, if taken first, would
have the greatest impact across the programme. This should emerge from the insights
above, not repeat them — it is the synthesis of the synthesis.

Tone: professional and policy-facing, written for the board of Futuro Digital LatAm.
Avoid generic language. Every claim must be traceable to a specific number or finding.
