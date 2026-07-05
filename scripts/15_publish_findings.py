"""
15_publish_findings.py — Publica / actualiza los 19 hallazgos en Notion.

Estrategia: IDs persistentes en .claude/notion_ids.json
- Si el ID ya existe para un título → actualiza esa página directamente (no busca)
- Si no existe → crea entrada nueva y guarda el ID
- Nunca crea duplicados, conserva historial/comentarios/checkboxes de Notion
- Funciona aunque el pipeline genere más findings en el futuro
"""
import sys, json, time, urllib.request, urllib.error, os
sys.stdout.reconfigure(encoding="utf-8")

TOKEN  = "ntn_b65450758806zVyAKVBTXBNw3EuRIE9M7oW7fCcTRssazc"
DB_ID  = "3941861d-eea8-81d2-aa1e-c187e058bc31"
IDS_FILE = ".claude/notion_ids.json"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Property IDs — evitan problemas de encoding con tildes
PROP_TITULO    = "title"
PROP_STAT      = "JJOr"
PROP_ALCANCE   = "%3FyxD"
PROP_PRIORIDAD = "Lv%3Dm"

def api(method, path, data=None):
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:150]}")
        return None

def load_ids():
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_ids(ids):
    with open(IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)

def clear_blocks(page_id):
    r = api("GET", f"/blocks/{page_id}/children")
    if not r:
        return
    for b in r.get("results", []):
        api("DELETE", f"/blocks/{b['id']}")

def make_props(f):
    return {
        PROP_TITULO:    {"title":     [{"text": {"content": f["titulo"]}}]},
        PROP_STAT:      {"rich_text": [{"text": {"content": f["stat"]}}]},
        PROP_ALCANCE:   {"rich_text": [{"text": {"content": f["alcance"]}}]},
        PROP_PRIORIDAD: {"select":    {"name": f["prioridad"]}},
    }

def make_blocks(f):
    return [
        {"object":"block","type":"callout","callout":{
            "rich_text":[{"type":"text","text":{"content": f["stat"]}}],
            "icon":{"type":"emoji","emoji":"📊"}}},
        {"object":"block","type":"paragraph","paragraph":{
            "rich_text":[{"type":"text","text":{"content": f["interp"]}}]}},
        {"object":"block","type":"heading_2","heading_2":{
            "rich_text":[{"type":"text","text":{"content":"Próximos pasos"}}]}},
        {"object":"block","type":"paragraph","paragraph":{
            "rich_text":[{"type":"text","text":{"content": f["rec"]}}]}},
    ]

def upsert(f, ids):
    props  = make_props(f)
    blocks = make_blocks(f)
    pid    = ids.get(f["titulo"])

    if pid:
        # ID conocido → actualizar directamente, sin búsqueda
        r = api("PATCH", f"/pages/{pid}", {"properties": props})
        if r:
            clear_blocks(pid)
            api("PATCH", f"/blocks/{pid}/children", {"children": blocks})
            print(f"  ✓ Actualizado — {f['titulo'][:65]}")
        else:
            print(f"  ✗ Error al actualizar — {f['titulo'][:65]}")
    else:
        # Primera vez → crear y guardar ID
        r = api("POST", "/pages", {
            "parent": {"database_id": DB_ID},
            "properties": props,
            "children": blocks
        })
        if r:
            ids[f["titulo"]] = r["id"]
            print(f"  ✓ Creado — {f['titulo'][:65]}")
        else:
            print(f"  ✗ Error al crear — {f['titulo'][:65]}")
    time.sleep(0.35)

# ── Limpieza opcional: archiva todas las entradas huérfanas ───────────────────
def cleanup_orphans(ids):
    """Archiva entradas en Notion que no están en notion_ids.json."""
    known = set(ids.values())
    all_entries = []
    cursor = None
    while True:
        body = {"start_cursor": cursor} if cursor else {}
        r = api("POST", f"/databases/{DB_ID}/query", body)
        if not r:
            break
        all_entries.extend(r.get("results", []))
        if r.get("has_more"):
            cursor = r["next_cursor"]
        else:
            break

    orphans = [e for e in all_entries if e["id"] not in known]
    if orphans:
        print(f"\nArchivando {len(orphans)} entradas huérfanas...")
        for e in orphans:
            api("PATCH", f"/pages/{e['id']}", {"archived": True})
            time.sleep(0.2)
        print(f"  ✓ {len(orphans)} entradas archivadas")
    else:
        print("\nNo hay entradas huérfanas.")

# ── 19 hallazgos ──────────────────────────────────────────────────────────────
FINDINGS = [
  {"titulo":"F1: Diferencias de Ingreso por País",
   "stat":"Brasil $1,458/mes vs Argentina $798/mes — brecha del 83%",
   "alcance":"6 países", "prioridad":"Alta",
   "interp":"Brasil lidera con ingreso mediano de $1,458 USD/mes; Argentina registra el mínimo con $798 USD/mes. Chile ($1,246) y México ($1,067) ocupan la franja media-alta; Colombia ($857) y Perú ($822) se acercan a Argentina. La dispersión interna también varía: Brasil tiene desviación estándar de $592 frente a $189 de Colombia.",
   "rec":"Calibrar todos los módulos de metas de ahorro usando porcentajes del ingreso local, no valores en USD. Definir una tabla de referencia por país que el facilitador use para adaptar los ejercicios en tiempo real."},
  {"titulo":"F2: Edad vs. Tasa de Ahorro",
   "stat":"r = +0.408, IC 95% [+0.332, +0.479] — 29–32 años: tasa 16% vs 18–22 años: 6%",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"Los respondentes de 29–32 años ahorran $154/mes en promedio (tasa 16%) frente a $61/mes del grupo de 18–22 (tasa 6%), con ingreso promedio prácticamente idéntico ($993 vs $1,039). La correlación r = +0.408 con IC 95% bien separado del cero confirma la relación. El F7 verifica que edad e ingreso no están relacionados (r = -0.029, p = 0.519), por lo que la brecha es conductual, no económica.",
   "rec":"Diseñar módulo de formación de hábito de ahorro para 18–22 años centrado en automatización: transferencia fija del 5% el día de cobro. Medir adherencia a 90 días como indicador primario, no el monto ahorrado."},
  {"titulo":"F3: Desglose de Gastos por Categoría",
   "stat":"Vivienda 28.5% + Alimentación 23.8% = 52.3% del ingreso",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"Vivienda y alimentación absorben juntas el 52.3% del ingreso mensual. El entretenimiento representa apenas 8.7% y la salud 4.9%. Las proporciones son estables entre los cuatro grupos de edad (F8): vivienda oscila entre 27.5% y 29.1%, confirmando que el problema de bajo ahorro en jóvenes no es estructural sino de hábito.",
   "rec":"Incluir módulo de negociación de costos fijos antes de abordar el presupuesto discrecional. Las estrategias de 'recortar entretenimiento' tienen impacto marginal (8.7%); la palanca real está en reducir o renegociar vivienda."},
  {"titulo":"F4: Tarjetahabientes vs. No Tarjetahabientes",
   "stat":"d = +0.089 (pequeño) — tarjetahabientes ahorran 6.7% más con ingreso 1.5% mayor",
   "alcance":"Muestra completa", "prioridad":"Baja",
   "interp":"Los tarjetahabientes gastan 16.1% más en alimentación y 17.2% más en entretenimiento, pero también ahorran 6.7% más ($101.75 vs $95.39/mes). La diferencia de ingreso es de apenas 1.5% ($1,023 vs $1,008), estadísticamente insignificante. El OLS (AA2) confirma que el efecto desaparece al controlar por edad e ingreso: la tarjeta en sí no predice ahorro.",
   "rec":"Desarrollar módulo de crédito responsable orientado al uso como herramienta de flujo de caja: liquidar el total cada mes, usar la fecha de corte correctamente, y distinguir crédito como conveniencia vs crédito como financiamiento de consumo."},
  {"titulo":"F5: Uso de IA vs. Satisfacción Financiera",
   "stat":"r = +0.571, IC 95% [+0.509, +0.628] — alto uso IA: satisfacción 3.43 vs bajo uso: 2.05",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"Los usuarios de alto uso de IA (11+ hrs/sem, n=21) reportan satisfacción promedio de 3.43/5 frente a 2.05 de bajo uso (0–3h/sem). Su ingreso promedio es $1,750 vs $747/mes. La correlación r(IA vs ingreso) = +0.634 es más fuerte que la correlación con satisfacción, y el F10 muestra que los usuarios de IA alta son top earners dentro de cada industria — el ingreso precede al uso de IA.",
   "rec":"Pilotar módulo de alfabetización en IA financiera como experimento controlado (grupo con módulo vs grupo sin módulo) midiendo satisfacción y ahorro a 6 meses, para determinar si el beneficio es del módulo o del perfil de ingreso preexistente."},
  {"titulo":"F6: Carga de Vivienda por País",
   "stat":"Argentina 34.1% vs Perú 24.6% — diferencia estructural de 9.5 puntos porcentuales",
   "alcance":"6 países", "prioridad":"Alta",
   "interp":"Argentina (34.1%) y Chile (32.6%) enfrentan las cargas de vivienda más altas, casi 10 puntos por encima de Perú (24.6%). Argentina no es el país de menor ingreso — Colombia ($857) y Perú ($822) tienen ingresos similares con cargas de 25.4% y 24.6% respectivamente. La presión de vivienda responde a condiciones del mercado inmobiliario, no al nivel de ingresos.",
   "rec":"Para Argentina y Chile: complementar currículo base con módulo de gestión de carga de vivienda (contratos, derechos del inquilino, vivienda compartida). Para Perú y Colombia: módulo que reencuadre explícitamente el margen liberado como oportunidad de ahorro."},
  {"titulo":"F7: Edad No Predice el Ingreso (Validación)",
   "stat":"r = -0.029, p = 0.519 — no hay relación estadísticamente significativa",
   "alcance":"Muestra completa", "prioridad":"Baja",
   "interp":"Pearson r(edad vs ingreso) = -0.029, p = 0.519. Los ingresos promedio por grupo de edad son casi idénticos: 18–22 ($1,039), 23–25 ($978), 26–28 ($1,066), 29–32 ($993). Este hallazgo de ausencia es la pieza que hace coherente el F2: la brecha de ahorro no puede atribuirse a que los mayores ganen más.",
   "rec":"Este hallazgo valida la recomendación del F2 sin generar módulo propio. Permite argumentar con evidencia que el módulo de ahorro automatizado para 18–22 años es la intervención de mayor retorno, porque esta población tiene capacidad económica comprobada."},
  {"titulo":"F8: Proporciones de Gasto Estables por Edad (Validación)",
   "stat":"Variación máxima en vivienda: 1.6pp (27.5%–29.1%); en entretenimiento: 0.4pp",
   "alcance":"Muestra completa", "prioridad":"Baja",
   "interp":"Las proporciones de gasto por categoría son prácticamente idénticas entre los cuatro grupos de edad. Vivienda oscila entre 27.5% y 29.1%; alimentación entre 23.6% y 24.1%; ninguna categoría muestra tendencia creciente o decreciente con la edad. Los jóvenes de 18–22 no gastan más proporcionalmente — simplemente ahorran menos de lo que les queda.",
   "rec":"Permite descartar que el módulo más importante para 18–22 años sea 'control de gastos discrecionales'. La evidencia apunta a que ahorro automatizado antes de cualquier gasto es el módulo más efectivo."},
  {"titulo":"F9: Ingreso por Industria",
   "stat":"Medianas sectoriales: $915 (Marketing) a $1,066 (RRHH); Finanzas dispersión $300–$2,874",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"Las medianas sectoriales varían apenas $151 entre industrias. Sin embargo, la dispersión interna es dramática: Finanzas muestra ingresos de $300 a $2,874; Tecnología de $300 a $2,092. La industria elegida predice poco el ingreso mediano en etapa temprana de carrera; la posición dentro de esa industria lo predice todo.",
   "rec":"En el diagnóstico inicial, incluir pregunta de posición relativa ('¿tus ingresos son más altos, similares o más bajos que colegas con la misma experiencia?') como proxy de posición en la distribución sectorial para personalizar metas de ahorro."},
  {"titulo":"F10: Usuarios de IA Alta dentro de la Distribución de Ingreso por Industria",
   "stat":"r(IA vs ingreso) = +0.634, p < 0.001 — ingresos 54%–143% por encima de mediana sectorial",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"Los 21 usuarios de alto uso de IA (11+ hrs/sem) se concentran en el extremo superior de la distribución de ingresos en cada sector. Su ingreso promedio supera la mediana de su industria entre 53.9% (Salud) y 142.7% (Educación). Esto fortalece la interpretación de que el alto ingreso precede al uso intensivo de IA, más que al revés.",
   "rec":"No asumir que un módulo de IA financiera por sí solo mejorará resultados de participantes de ingreso bajo-medio. Pilotarlo como experimento controlado (ver F5) antes de escalar."},
  {"titulo":"F11: Cuenta de Ahorro vs. Comportamiento Real",
   "stat":"r = +0.014, p = 0.760 — tener cuenta de ahorro no predice ahorrar más",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"Los respondentes con cuenta de ahorro (n=362) ahorran apenas 3% más que quienes no tienen una ($100 vs $97/mes) con solo 0.5% más de ingreso. La correlación r = 0.014 (p = 0.760) es estadísticamente indistinguible de cero. El 72.4% tiene cuenta de ahorro — el instrumento está disponible pero no se usa.",
   "rec":"No diseñar módulos orientados a 'abrir una cuenta de ahorro' como meta en sí misma. El módulo debe centrarse en el comportamiento de transferencia automática. La meta medible es 'transferencia configurada y ejecutada el primer mes', no 'cuenta abierta'."},
  {"titulo":"F12: Deuda Activa vs. Ahorro y Satisfacción",
   "stat":"d = -0.108 en satisfacción — deudores ahorran 5% más pero reportan 2.7% menos satisfacción",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"Los respondentes con deuda activa (n=234, deuda promedio $3,952) ahorran marginalmente más ($101 vs $97/mes) pero reportan menor satisfacción (2.46 vs 2.53). La correlación deuda vs ahorro es r = 0.026 (p = 0.564), no significativa. La deuda opera principalmente como carga psicológica, no como restricción de flujo de caja.",
   "rec":"Diseñar módulo de gestión de deuda orientado al bienestar percibido: técnicas de priorización (avalancha vs bola de nieve), comunicación de progreso visible, y separación mental entre 'deuda bajo control' y 'deuda problemática'."},
  {"titulo":"F13: Meta Financiera vs. Tasa de Ahorro Real",
   "stat":"Retiro 8.0% vs Viaje 10.8% — metas concretas producen 35% más ahorro que metas abstractas",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"'Ahorrar para viaje' (10.8%), 'Fondo de emergencia' (11.0%) y 'Comprar casa' (10.5%) lideran en tasa de ahorro. 'Ahorrar para retiro' (8.0%) y 'Estudiar posgrado' (8.4%) registran las tasas más bajas. Los ingresos entre grupos son comparables ($941–$1,080), por lo que la diferencia no se explica por capacidad económica.",
   "rec":"Estructurar el módulo de metas en dos niveles: primero meta concreta de horizonte corto (3–12 meses) que genere el hábito, y solo después introducir metas de largo plazo como el retiro. El progreso visible hacia una meta cercana es el mecanismo que sostiene el hábito."},
  {"titulo":"F14: Tarjetahabientes — Gasto Desglosado por Categoría",
   "stat":"Alimentación +16.1% ($258 vs $222) y Entretenimiento +17.2% ($95 vs $81) — Vivienda solo +1.4%",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"El gasto adicional de tarjetahabientes se concentra en alimentación (+16.1%) y entretenimiento (+17.2%). Las categorías estructurales son casi idénticas: vivienda (+1.4%), transporte (+3.9%), salud (+4.8%). El gasto extra es discrecional y acotado: no redefine la estructura de gasto, solo la amplía en el margen.",
   "rec":"En el módulo de crédito responsable, usar esta distribución como caso de enseñanza: el gasto extra es discrecional (+16–17% en alimentos y entretenimiento) pero no afecta el ahorro (+6.7%). La discusión debe centrarse en cuándo el gasto con tarjeta supera el ingreso disponible."},
  {"titulo":"F15: Meta Financiera × Grupo de Edad (Interacción)",
   "stat":"Bolsa r=+0.634 en 29–32 (tasa 20.1%); Emergencia mejor a 18–22 (tasa 10.4%)",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"La meta óptima cambia con la edad: a 18–22 años 'Fondo de emergencia' produce la mayor tasa (10.4%); a 29–32 años 'Invertir en bolsa' lidera con 20.1% y correlación r=+0.634 (p<0.001). Asignar la meta equivocada al grupo equivocado produce la peor combinación posible — 'Invertir en bolsa' a 18–22 años tiene tasa de apenas 3.1%.",
   "rec":"Implementar sistema de asignación de meta por etapa de vida en el diagnóstico inicial. Para 18–22: fondo de emergencia o viaje. Para 29–32: inversión. No presentar las mismas metas a todos los grupos de edad."},
  {"titulo":"F16: Paradoja de la Satisfacción Financiera",
   "stat":"r(satisfacción→tasa ahorro) = -0.149, IC [-0.234, -0.062] — mayor satisfacción predice menor tasa de ahorro",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"La satisfacción financiera correlaciona negativamente con la tasa de ahorro (r = -0.149, p < 0.001), pero positivamente con el ingreso (r = +0.581). Los más satisfechos financieramente tienen más ingreso pero ahorran una proporción menor de él. La paradoja se resuelve porque quienes tienen más ingreso y satisfacción pueden permitirse gastar más en términos absolutos manteniendo el mismo nivel de vida.",
   "rec":"No usar la satisfacción financiera como proxy de comportamiento de ahorro saludable en el diagnóstico. Diseñar indicadores compuestos que combinen satisfacción, tasa de ahorro y progreso hacia metas concretas."},
  {"titulo":"F17: Triángulo de la IA (Ingreso, Satisfacción, Ahorro)",
   "stat":"r(IA→tasa ahorro) = -0.136, IC [-0.221, -0.049] — mayor uso IA correlaciona con menor tasa de ahorro",
   "alcance":"Muestra completa", "prioridad":"Alta",
   "interp":"Los usuarios de IA ganan más (r=+0.634), se sienten más satisfechos (r=+0.571), pero ahorran una proporción menor de su ingreso (r=-0.136, p=0.002). La IA correlaciona con mayor consumo relativo, no con mayor ahorro proporcional. El triángulo es consistente: mayor ingreso → mayor satisfacción → menor necesidad percibida de ahorrar más.",
   "rec":"Al presentar el módulo de IA financiera, ser explícito sobre la paradoja: las herramientas de IA pueden mejorar la percepción financiera sin necesariamente mejorar el comportamiento de ahorro. Combinar el módulo de IA con el de metas concretas y transferencia automática."},
  {"titulo":"F18: Educación — Inversión Absoluta vs. Carga Relativa",
   "stat":"r(gasto absoluto→satisfacción) = +0.249 vs r(% ingreso→satisfacción) = -0.203",
   "alcance":"Muestra completa", "prioridad":"Media",
   "interp":"El gasto en educación en USD absolutos correlaciona positivamente con la satisfacción financiera (r=+0.249, p<0.001), pero el porcentaje del ingreso destinado a educación correlaciona negativamente (r=-0.203, p<0.001). Gastar más en educación se asocia con mayor bienestar cuando el ingreso es alto; pero cuando representa un porcentaje alto del ingreso, se convierte en presión.",
   "rec":"En el módulo de educación financiera, distinguir entre inversión en desarrollo profesional (deseable, aumenta satisfacción) y sobre-extensión educativa como porcentaje del ingreso (predice menor satisfacción). Establecer una regla práctica: educación no debe superar el 10–12% del ingreso mensual."},
  {"titulo":"F19: Patrón Edad-Ahorro Universal Excepto Argentina",
   "stat":"5 de 6 países pasan FDR (r=0.38–0.48); Argentina r=+0.273 p=0.022, no pasa BH",
   "alcance":"6 países", "prioridad":"Media",
   "interp":"En 5 de los 6 países el patrón edad→tasa_ahorro es robusto y pasa la corrección FDR: Colombia r=+0.444, Perú r=+0.484, México r=+0.435, Chile r=+0.419, Brasil r=+0.387. Argentina muestra correlación positiva (r=+0.273, p=0.022) pero no pasa el umbral BH (threshold 0.017). El OLS por país confirma: Argentina tiene R²=0.085 vs Perú R²=0.267, sugiriendo factores macroeconómicos estructurales.",
   "rec":"Para Argentina, diseñar un módulo complementario de resiliencia financiera ante volatilidad macroeconómica. El patrón de acumulación gradual de hábito con la edad existe pero es más débil — probablemente perturbado por inflación y devaluación estructural."},
]

# ── Main ──────────────────────────────────────────────────────────────────────
print(f"Cargando IDs desde {IDS_FILE}...")
ids = load_ids()
print(f"  {len(ids)} IDs conocidos\n")

print(f"Publicando {len(FINDINGS)} hallazgos...")
for f in FINDINGS:
    upsert(f, ids)

save_ids(ids)
print(f"\nIDs guardados en {IDS_FILE}")

cleanup_orphans(ids)

total_known = len(ids)
print(f"\n✓ Listo — {total_known} hallazgos en Notion, {IDS_FILE} actualizado")
