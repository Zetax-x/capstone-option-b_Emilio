"""
14_finalize.py — Sincroniza analysis-report.md y 05_interpret.md
con los charts que realmente existen en disco.

Corre siempre como ULTIMO paso del pipeline (después de country_profiles.py).
Elimina cualquier desincronización entre los números de chart generados
y las referencias escritas en los documentos.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import re
import glob

CHARTS_DIR  = "charts"
REPORT_PATH = "analysis-report.md"
INTERP_PATH = "scripts/05_interpret.md"

# ── 1. Leer charts reales en disco ────────────────────────────────────────────
png_files = sorted(
    glob.glob(f"{CHARTS_DIR}/*.png"),
    key=lambda p: int(re.match(r".*[/\\](\d+)_", p).group(1))
               if re.match(r".*[/\\](\d+)_", p) else 0
)
total = len(png_files)

# Mapa: nombre-contenido → (número, basename)
# "savings_rate_vs_income_by_age.png" → (19, "19_savings_rate_vs_income_by_age.png")
disk = {}
for path in png_files:
    base = os.path.basename(path)
    m = re.match(r"^(\d+)_(.+)$", base)
    if m:
        disk[m.group(2)] = (int(m.group(1)), base)

print(f"Charts en disco: {total}")

# ── 2. Leer archivos ──────────────────────────────────────────────────────────
with open(REPORT_PATH, encoding="utf-8") as f:
    report = f.read()

with open(INTERP_PATH, encoding="utf-8") as f:
    interp = f.read()

# ── 3. Extraer descripciones de la tabla actual del reporte ───────────────────
# Formato: | 38 | `38_savings_rate_vs_income_by_age.png` | Desc | Script | Hall |
ROW_RE = re.compile(
    r"\| *(\d+) *\| *`(\d+_[^`]+\.png)` *\| *([^|]+?) *\| *([^|]+?) *\| *([^|]+?) *\|"
)
descriptions = {}   # content_name → (desc, script, hallazgo)
for m in ROW_RE.finditer(report):
    content = re.sub(r"^\d+_", "", m.group(2))
    descriptions[content] = (m.group(3).strip(), m.group(4).strip(), m.group(5).strip())

# ── 4. Construir nueva tabla ──────────────────────────────────────────────────
new_rows = []
for path in png_files:
    base = os.path.basename(path)
    m = re.match(r"^(\d+)_(.+)$", base)
    if not m:
        continue
    num, content = int(m.group(1)), m.group(2)
    if content in descriptions:
        desc, script, hallazgo = descriptions[content]
    else:
        desc    = content.replace("_", " ").replace(".png", "")
        script  = "—"
        hallazgo = "—"
    new_rows.append(f"| {num:02d} | `{base}` | {desc} | {script} | {hallazgo} |")

# ── 5. Reemplazar tabla en el reporte ─────────────────────────────────────────
TABLE_BLOCK_RE = re.compile(
    r"(\| # \| Archivo \| Descripción \| Script \| Hallazgo \|\n"
    r"\|[-| ]+\|\n)"     # separator row
    r"([\s\S]+?)"
    r"(\n\n---)",
    re.MULTILINE
)
m_table = TABLE_BLOCK_RE.search(report)
if m_table:
    replacement = m_table.group(1) + "\n".join(new_rows) + m_table.group(3)
    report = report[:m_table.start()] + replacement + report[m_table.end():]
    print(f"Tabla de charts actualizada ({len(new_rows)} filas)")
else:
    print("ADVERTENCIA: no se encontró la tabla de charts — verifica el formato del reporte")

# ── 6. Actualizar contadores de charts en el reporte ─────────────────────────
# Patrón genérico: cualquier "N charts (01–N)" o "N visualizaciones (charts 01–N)"
def replace_count(text, n):
    text = re.sub(
        r"\b\d+ charts \(01[–\-]\d+\)",
        f"{n} charts (01–{n:02d})",
        text
    )
    text = re.sub(
        r"\b\d+ gráficas en total \(charts \d+[–\-]\d+\)",
        f"{n} gráficas en total (charts 01–{n:02d})",
        text
    )
    text = re.sub(
        r"\*\*(\d+) visualizaciones en total\*\* \(charts \d+[–\-]\d+\)",
        f"**{n} visualizaciones en total** (charts 01–{n:02d})",
        text
    )
    text = re.sub(
        r"\*\*(\d+) visualizaciones\*\*,",
        f"**{n} visualizaciones**,",
        text
    )
    return text

report = replace_count(report, total)
print(f"Contadores actualizados a {total}")

# ── 7. Guardar reporte ────────────────────────────────────────────────────────
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)
print(f"Guardado: {REPORT_PATH}")

# ── 8. Actualizar referencias de charts en 05_interpret.md ───────────────────
def fix_chart_ref(m):
    old_base = m.group(1)
    content  = re.sub(r"^\d+_", "", old_base)
    if content in disk:
        return f"charts/{disk[content][1]}"
    return m.group(0)   # no cambiar si no está en disco

updated_interp = re.sub(r"charts/(\d+_[\w.]+\.png)", fix_chart_ref, interp)

changed = updated_interp != interp
with open(INTERP_PATH, "w", encoding="utf-8") as f:
    f.write(updated_interp)

refs_fixed = len(re.findall(r"charts/\d+_[\w.]+\.png", interp)) if changed else 0
print(f"{'Referencias actualizadas' if changed else 'Sin cambios'} en: {INTERP_PATH}")

# ── 9. Resumen ────────────────────────────────────────────────────────────────
print(f"\n✓ Pipeline finalizado — {total} charts, documentos sincronizados")
