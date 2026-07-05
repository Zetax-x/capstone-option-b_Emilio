# Pipeline: Análisis LatAm 2025

## Project
Repeatable financial wellness analysis pipeline for Futuro Digital LatAm.
Dataset: data/latam_finanzas_2025.csv (raw) → data/latam_finanzas_clean.csv (clean)
Report: analysis-report.md

## Python Environment
Activate venv before running any script: `venv\Scripts\activate`
Libraries: pandas, matplotlib, seaborn, scipy, numpy (versions pinned in requirements.txt)
Scripts go in scripts/. Charts go in charts/ as PNGs.

**Auto-setup rule (critical):** Before running ANY Python script, check if `venv\Scripts\activate.bat` exists.
- If it does NOT exist: run `setup.bat` automatically without asking the user, wait for it to complete, then proceed.
- If it exists: activate with `venv\Scripts\activate` and proceed normally.
Never ask the user to run setup.bat manually — handle it transparently.

## Actualización automática del reporte
Cada vez que se descubra un nuevo hallazgo, se genere un nuevo chart, o se corra cualquier script que produzca resultados estadísticos nuevos, actualizar `analysis-report.md` automáticamente con:
- El nuevo hallazgo en la Sección 4 (Hallazgos) con su chart referenciado
- Una nueva recomendación en la Sección 6 si el hallazgo lo justifica
- Los valores reales en la Sección 5 (Análisis Avanzado) si provienen de 07_advanced.py
- La Conclusión General actualizada si el nuevo hallazgo cambia las síntesis existentes

No esperar instrucción explícita del usuario para hacer esta actualización.

## Integridad del pipeline — regla crítica

**El pipeline es una cadena, no un menú.** Cada fase produce outputs que las fases siguientes consumen. Si se actualiza solo una parte, los outputs posteriores quedan desactualizados y el proyecto entra en estado inconsistente. Esto es un error de diseño, no un atajo válido.

Reglas concretas:
- Si cambia el dataset (Fase 1–2) → hay que reejecutar todas las fases desde la 3.
- Si cambia el análisis estadístico (Fase 3) → hay que reejecutar visualizaciones (4), correlaciones (5), análisis avanzado (6), interpretaciones (7), hallazgo destacado (8) y publicación (9).
- Si cambia una gráfica (Fases 4–6) → hay que reejecutar la interpretación (7), el script de hallazgo destacado (8) y verificar las referencias en `analysis-report.md`.
- Si cambia la interpretación (Fase 7) → hay que correr la Fase 8 (08_featured.py) para regenerar el bloque rotativo y actualizar `analysis-report.md`.
- **Nunca** actualizar `analysis-report.md` o `05_interpret.md` manualmente sin haber corrido las fases de análisis previas — el documento debe reflejar los resultados reales del pipeline, no valores escritos a mano.

La única operación segura es correr el pipeline completo desde la fase que cambió hasta el final.

## Reset del pipeline
Si el usuario dice "reinicia", "reinicia el pipeline", "corre desde cero" o similar:
1. Correr `scripts/00_reset.py` primero — borra todos los charts y resetea el contador a 0
2. Luego correr el pipeline completo desde la Fase 1

No correr `00_reset.py` en ningún otro caso. No preguntar confirmación — si el usuario dijo "desde cero", proceder directamente.

## Quick start
Si el usuario no especifica qué hacer, preséntale estas opciones:

1. **Correr el pipeline completo** — ejecuta todas las fases en orden (1-8) sin pedir confirmación entre cada una
2. **Correr desde una fase específica** — el usuario elige el punto de entrada; se ejecutan esa fase y todas las posteriores
3. **Ver estado actual** — ejecuta `.claude/hooks/validate-phases.sh` y muestra qué fases están completas y cuáles faltan

Si el usuario dice "corre todo", "ejecuta el pipeline", "arranca" o similar → ejecuta todas las fases en orden sin interrupciones, incluyendo /interpret (Fase 7).
Si el usuario dice "qué falta" o "estado" → corre el validador primero y sugiere la siguiente fase pendiente.
Si el usuario dice "actualiza X" sin especificar fase → pregunta desde qué fase debe arrancar antes de ejecutar nada.

## Anuncio de trabajo en curso

Antes de cada acción sobre un archivo (leer, editar, escribir, ejecutar un script), mostrar siempre una línea de texto con este formato:

```
[Paso N/total] Archivo: nombre_del_archivo — qué se va a hacer
```

Ejemplos:
```
[Paso 1/3] Archivo: CLAUDE.md — agregando instrucción de notificaciones de progreso
[Paso 2/3] Archivo: analysis-report.md — actualizando valores reales de OLS en Sección 5.2
[Paso 3/3] Archivo: scripts/07_advanced.py — corrigiendo numeración de chart
```

Si es la ejecución de un script (Bash), usar:
```
[Ejecutando] scripts/03_analyse.py — análisis estadístico de 14 hallazgos
```

Este anuncio va siempre ANTES de la llamada a la herramienta, no después. Si hay varios archivos en paralelo, listarlos todos antes de ejecutar.

## Notificaciones de progreso del pipeline

Después de completar cada fase, antes de iniciar la siguiente, mostrar siempre un mensaje de progreso con este formato exacto:

```
✓ Fase [N] completa — [nombre del script o skill] ([resultado clave en una línea])
→ Iniciando Fase [N+1]: [qué hará]
```

Ejemplos:
```
✓ Fase 2 completa — 02_clean.py (500 filas limpias, 33 faltantes rellenados)
→ Iniciando Fase 3: análisis estadístico de 14 hallazgos
```
```
✓ Fase 4 completa — 04_visualise.py (12 charts generados, .last_chart=12)
→ Iniciando Fase 5: correlaciones cruzadas por país
```

Al terminar la Fase 8 (última), mostrar:
```
✓ Pipeline completo — [N] charts, [N] hallazgos interpretados, analysis-report.md actualizado
```

Este mensaje va en texto plano en la respuesta de Claude, no requiere herramienta.

## Pipeline — Orden de ejecución
Correr los scripts en este orden exacto (el auto-numerado de charts depende de la secuencia):

| Fase | Script | Output |
|------|--------|--------|
| 1 | scripts/01_explore.py | Exploración inicial del dataset |
| 2 | scripts/02_clean.py | data/latam_finanzas_clean.csv |
| 3 | scripts/03_analyse.py | 14 hallazgos en consola (obligatorios + auto-expansión + brechas) |
| 4 | scripts/04_visualise.py | charts/01 a charts/12 |
| 5 | scripts/06_correlations.py | charts/13 y charts/14 (correlaciones cruzadas) |
| 6 | scripts/07_advanced.py | charts/15 a charts/19 (negativos, OLS, clustering, FDR, ahorro×ingreso) |
| 7 | scripts/08_featured.py | Bloque "Hallazgo Destacado" en analysis-report.md (rotativo por fecha) |
| 8 | scripts/09_explore_new.py | exploración adicional (sin charts) |
| 9 | scripts/10_findings_new.py | charts/20-21 (meta×edad, deuda×ahorro) |
| 10 | scripts/11_explore_more.py | charts/22-29 (correlaciones FDR: IA, edad×ahorro por país) |
| 11 | scripts/12_deeper_stats.py | charts/30-34 (IC95%, Cohen's d, OLS por país) |
| 12 | scripts/13_country_charts.py | charts/35-38 (perfiles por país) |
| 13 | scripts/country_profiles.py | scripts/country_profiles.md |
| 14 | scripts/14_finalize.py | Sincroniza analysis-report.md y 05_interpret.md con los charts reales |
| 15 | /publish-finding skill | Notion Findings Tracker (**manual** — no corre automáticamente) |

**Regla crítica:** scripts/14_finalize.py SIEMPRE corre como último paso obligatorio antes de publicar.
Sincroniza automáticamente el índice de charts y todas las referencias de rutas en los documentos.
Sin él, cualquier desincronización entre los números de chart y el reporte queda sin corregir.

Country scripts: country_profiles.py → scripts/country_profiles.md

## Notion Workspace
Integration: LatAm Pipeline
Databases: "Findings Tracker", "Country Profiles"
Report page: "Informe Ejecutivo"

**La publicación a Notion es manual.** No se dispara automáticamente al terminar el pipeline.
Para publicar los hallazgos, pedir explícitamente: "corre /publish-finding".
Esto evita que Notion se actualice sin confirmación en cada ejecución del pipeline.

## Perfil del analista
El análisis es producido por un analista de datos con capacidad para explicar conceptos estadísticos a cualquier tipo de lector. El estándar de claridad es: si un estudiante de preparatoria o alguien sin ningún conocimiento previo de estadística no puede entender la explicación, no está suficientemente explicada.

Reglas concretas:
- Cada término técnico (correlación, regresión, p-valor, cluster, IC 95%, FDR, coeficiente, desviación estándar, etc.) debe explicarse en lenguaje cotidiano la primera vez que aparece, usando una analogía o ejemplo del mundo real si es necesario.
- Las notas se marcan con 📝 *Nota metodológica:* y van inmediatamente después del término técnico.
- Los números siempre van acompañados de su significado en palabras: no solo "r = 0.57" sino "r = 0.57, lo que significa que la relación es moderada-fuerte y positiva".
- Nunca asumir que el lector sabe qué es una media, una mediana, una correlación, un intervalo de confianza o una regresión. Siempre explicar.

## Pipeline Components
Hooks: chart counter, script logger, phase validator (configured in .claude/settings.json)
Skills: /interpret (finding format), /publish-finding (Notion push)
Agent: country-profiler (parallel country analysis)
