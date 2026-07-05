#!/bin/bash
echo "=== Pipeline Status ==="

# Fase 2 — Limpieza
[ -f data/latam_finanzas_clean.csv ] && echo "✓ Fase 2: Dataset limpio" || echo "✗ Fase 2: latam_finanzas_clean.csv faltante"

# Fase 2.5 — Agente de perfiles
[ -f .claude/agents/country-profiler.md ] && echo "✓ Fase 2.5: Agente country-profiler" || echo "✗ Fase 2.5: Agente faltante"

# Fase 3 — Análisis (14 hallazgos)
[ -f scripts/03_analyse.py ] && echo "✓ Fase 3: Script de análisis" || echo "✗ Fase 3: 03_analyse.py faltante"

# Fase 4 — Visualizaciones base (charts 01-12)
n4=$(ls charts/0[1-9]_*.png charts/1[0-2]_*.png 2>/dev/null | wc -l)
[ "$n4" -ge 12 ] && echo "✓ Fase 4: $n4/12 charts de análisis" || echo "✗ Fase 4: solo $n4/12 charts (correr 04_visualise.py)"

# Fase 5 — Correlaciones cruzadas (charts 13-14)
n5=$(ls charts/13_*.png charts/14_*.png 2>/dev/null | wc -l)
[ "$n5" -ge 2 ] && echo "✓ Fase 5: $n5/2 charts de correlación" || echo "✗ Fase 5: $n5/2 charts (correr 06_correlations.py)"

# Fase 6 — Análisis avanzado (charts 15-18)
n6=$(ls charts/1[5-8]_*.png 2>/dev/null | wc -l)
[ "$n6" -ge 4 ] && echo "✓ Fase 6: $n6/4 charts avanzados" || echo "✗ Fase 6: $n6/4 charts (correr 07_advanced.py)"

# Fase 7 — Interpretaciones
[ -f scripts/05_interpret.md ] && echo "✓ Fase 7: Interpretaciones (05_interpret.md)" || echo "✗ Fase 7: Interpretaciones faltantes (correr /interpret)"

# Reporte ejecutivo
[ -f analysis-report.md ] && echo "✓ Reporte: analysis-report.md" || echo "✗ Reporte: analysis-report.md faltante"

# Total de charts
total=$(ls charts/*.png 2>/dev/null | wc -l)
echo "--- Total charts generados: $total/18 ---"
