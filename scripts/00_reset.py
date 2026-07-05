"""
00_reset.py — Reinicia el pipeline desde cero.
Borra todos los charts generados y resetea el contador .last_chart a 0.
Solo debe correrse cuando el usuario dice explicitamente "reinicia" o "corre desde cero".
"""

import os
import sys
import glob
sys.stdout.reconfigure(encoding="utf-8")

charts_dir = "charts"

# Borrar todos los PNGs
pngs = glob.glob(f"{charts_dir}/*.png")
for f in pngs:
    os.remove(f)

# Resetear contador
with open(f"{charts_dir}/.last_chart", "w") as f:
    f.write("0")

print(f"✓ {len(pngs)} charts eliminados")
print("✓ .last_chart reseteado a 0")
print("Pipeline listo para correr desde cero.")
