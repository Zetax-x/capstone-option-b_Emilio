# -*- coding: utf-8 -*-
"""
08_featured.py -- Hallazgo Destacado Rotativo
Selecciona un hallazgo distinto cada ejecucion y actualiza analysis-report.md.
Seed = fecha actual: mismo dia -> mismo hallazgo, dias distintos -> rotacion automatica.
"""

import random
import re
from datetime import date

random.seed(date.today().toordinal())

SPOTLIGHTS = [
    {
        "id": "F1", "subtitulo": "Hallazgo 1 -- Ingreso por Pais",
        "titulo": "El mismo manual no funciona en seis paises distintos",
        "narrativa": (
            "Un facilitador en Buenos Aires y uno en Sao Paulo pueden estar leyendo "
            "el mismo manual -- pero sus participantes viven en mundos economicos "
            "completamente distintos. Brasil tiene un ingreso mediano de $1,458/mes; "
            "Argentina, $798. La misma meta de 'ahorra $200 al mes' es alcanzable "
            "para uno y practicamente imposible para el otro. El programa necesita "
            "hablar en porcentajes del ingreso local, no en dolares."
        ),
        "cifra_clave": "83% de brecha entre Brasil ($1,458) y Argentina ($798)",
        "chart": "charts/01_income_by_country.png",
    },
    {
        "id": "F2", "subtitulo": "Hallazgo 2 -- Edad vs. Tasa de Ahorro",
        "titulo": "Tienen el mismo sueldo -- pero uno ahorra 2.7 veces mas",
        "narrativa": (
            "Un profesional de 22 anos y uno de 30 ganan practicamente lo mismo "
            "en esta muestra. Pero el de 30 ahorra 2.7 veces mas. No porque sea "
            "mas disciplinado -- sino porque lleva mas anos practicando el habito. "
            "El habito de ahorro se construye como un musculo: los jovenes de 18-22 "
            "no lo tienen todavia, no porque no puedan, sino porque nadie les mostro "
            "como entrenarlo desde el primer sueldo."
        ),
        "cifra_clave": "Tasa de ahorro: 6% a los 18-22 vs. 16% a los 29-32",
        "chart": "charts/02_age_vs_savings.png",
    },
    {
        "id": "F3", "subtitulo": "Hallazgo 3 -- Desglose de Gastos",
        "titulo": "Recortar entretenimiento no es la solucion",
        "narrativa": (
            "El consejo clasico de 'gasta menos en salidas' suena razonable -- "
            "pero los datos lo desmienten. El entretenimiento representa apenas "
            "el 8.7% del ingreso. Vivienda y alimentacion se llevan el 52.3%. "
            "Doblar la tasa de ahorro solo recortando entretenimiento significaria "
            "eliminar practicamente todo el ocio. La palanca real esta en negociar "
            "el arriendo, no en cancelar suscripciones."
        ),
        "cifra_clave": "52.3% del ingreso en vivienda + alimentacion; entretenimiento: 8.7%",
        "chart": "charts/03_spending_breakdown.png",
    },
    {
        "id": "F4", "subtitulo": "Hallazgo 4 -- Tarjetahabientes vs. No Tarjetahabientes",
        "titulo": "La tarjeta no es el enemigo",
        "narrativa": (
            "Durante anos, la educacion financiera popular trato la tarjeta de credito "
            "como el villano. Pero en esta muestra, quienes tienen tarjeta gastan MAS "
            "y ahorran MAS que quienes no la tienen, con practicamente el mismo ingreso. "
            "No es la tarjeta la que dana las finanzas -- es no saber usarla. "
            "La diferencia entre un instrumento y un problema es el comportamiento "
            "de quien lo sostiene."
        ),
        "cifra_clave": "+6.7% ahorro en tarjetahabientes con solo +1.5% mas de ingreso",
        "chart": "charts/04_satisfaction_by_ai_usage.png",
    },
    {
        "id": "F5", "subtitulo": "Hallazgo 5 -- IA vs. Satisfaccion Financiera",
        "titulo": "Las herramientas digitales estan cambiando quien llega primero",
        "narrativa": (
            "r = 0.571 entre uso de IA y satisfaccion financiera -- correlacion fuerte. "
            "Y a nivel de paises, r = 0.992: casi perfecta. Pero ojo: los usuarios "
            "intensivos de IA no son cualquier persona -- son los mejor pagados dentro "
            "de su sector (F10). La IA puede ser una palanca real, o puede ser el "
            "privilegio de quienes ya estaban mejor posicionados. Solo un experimento "
            "controlado puede separar las dos hipotesis."
        ),
        "cifra_clave": "r = 0.571 (individual), r = 0.992 (por pais)",
        "chart": "charts/04_satisfaction_by_ai_usage.png",
    },
    {
        "id": "F6", "subtitulo": "Hallazgo 6 -- Carga de Vivienda por Pais",
        "titulo": "Argentina y Chile tienen un problema que no es de habitos",
        "narrativa": (
            "En Argentina, la vivienda absorbe el 34.1% del ingreso. En Peru, el 24.6%. "
            "Esa diferencia de casi 10 puntos no la produce el comportamiento individual "
            "-- la produce el mercado inmobiliario. Un participante argentino que hiciera "
            "todo 'bien' seguiria enfrentando una restriccion estructural que su par "
            "peruano no enfrenta. El programa necesita reconocer esto antes de disenyar "
            "metas que parezcan alcanzables para todos por igual."
        ),
        "cifra_clave": "34.1% (Argentina) vs. 24.6% (Peru) de carga de vivienda",
        "chart": "charts/05_housing_burden_by_country.png",
    },
    {
        "id": "F7", "subtitulo": "Hallazgo 7 -- Edad No Predice el Ingreso",
        "titulo": "La edad no es una excusa -- es una oportunidad",
        "narrativa": (
            "Es facil asumir que los jovenes de 18-22 ahorran menos porque ganan menos. "
            "Los datos dicen exactamente lo contrario: r = -0.029, p = 0.519 -- la edad "
            "no predice el ingreso en absoluto. Los cuatro grupos de edad ganan "
            "practicamente lo mismo (~$978-$1,066). Eso significa que la brecha de "
            "ahorro no es una limitacion economica que el tiempo resolvera solo -- "
            "es una oportunidad de intervencion educativa que existe ahora mismo."
        ),
        "cifra_clave": "r = -0.029, p = 0.519 -- ingreso plano entre los cuatro grupos de edad",
        "chart": "charts/19_savings_rate_vs_income_by_age.png",
    },
    {
        "id": "F8", "subtitulo": "Hallazgo 8 -- Proporciones de Gasto Estables por Edad",
        "titulo": "No gastan mas -- simplemente no ahorran lo que les queda",
        "narrativa": (
            "Si los jovenes de 18-22 gastaran proporcionalmente mas en entretenimiento, "
            "el programa necesitaria ensenyarles autocontrol. Pero vivienda, alimentacion, "
            "transporte y entretenimiento representan practicamente los mismos porcentajes "
            "en todos los grupos de edad. El problema no esta en como gastan -- esta en "
            "que no convierten el margen disponible en ahorro. Es una omision, no un exceso."
        ),
        "cifra_clave": "Entretenimiento: 8.5%-8.9% identico en todos los grupos de edad",
        "chart": "charts/06_spending_by_age_group.png",
    },
    {
        "id": "F9", "subtitulo": "Hallazgo 9 -- Ingreso por Industria",
        "titulo": "La industria dice poco -- donde estas dentro de ella dice todo",
        "narrativa": (
            "Las medianas por industria van de $915 a $1,066 -- apenas $151 de diferencia. "
            "Pero dentro de Finanzas hay personas ganando $300 y otras ganando $2,874. "
            "Preguntar a alguien en que industria trabaja dice muy poco sobre sus finanzas. "
            "Lo que importa es donde esta dentro de esa industria. El programa deberia "
            "preguntar ambas cosas desde el primer dia para segmentar correctamente."
        ),
        "cifra_clave": "Finanzas: $300 a $2,874 dentro del mismo sector",
        "chart": "charts/07_income_by_industry.png",
    },
    {
        "id": "F10", "subtitulo": "Hallazgo 10 -- Usuarios de IA Alta por Industria",
        "titulo": "Los usuarios de IA no son un grupo aleatorio",
        "narrativa": (
            "Los 21 participantes que mas usan herramientas de IA no estan repartidos "
            "al azar entre las industrias -- estan concentrados en el extremo superior "
            "de la distribucion de ingresos de cada sector. En Educacion, su ingreso "
            "supera la mediana sectorial en 142.7%. El uso intensivo de IA no parece "
            "ser la causa del exito financiero -- parece ser su consecuencia."
        ),
        "cifra_clave": "Usuarios IA alta: 54%-143% por encima de la mediana sectorial",
        "chart": "charts/08_high_ia_by_industry.png",
    },
    {
        "id": "F11", "subtitulo": "Hallazgo 11 -- Cuenta de Ahorro vs. Comportamiento",
        "titulo": "Tener la cuenta no es suficiente",
        "narrativa": (
            "El 72.4% de los participantes tiene cuenta de ahorro. Y aun asi, "
            "quienes la tienen ahorran apenas un 3% mas -- diferencia estadisticamente "
            "indistinguible de cero (r = 0.014, p = 0.760). La cuenta es el recipiente, "
            "no el habito. Lo que importa no es abrirla -- es programar una transferencia "
            "automatica el dia de cobro para que el ahorro ocurra antes de que "
            "el dinero pueda gastarse."
        ),
        "cifra_clave": "r = 0.014, p = 0.760 -- la cuenta sola no predice nada",
        "chart": "charts/09_savings_account_vs_behaviour.png",
    },
    {
        "id": "F12", "subtitulo": "Hallazgo 12 -- Deuda vs. Ahorro y Satisfaccion",
        "titulo": "La deuda no restringe el flujo de caja -- restringe el bienestar",
        "narrativa": (
            "Los deudores de esta muestra ahorran un poco MAS que quienes no tienen "
            "deuda (r = 0.026, p = 0.564 -- no significativo). Pero reportan menos "
            "satisfaccion financiera (-2.7%). La deuda no vacia las cuentas -- vacia "
            "la tranquilidad. El programa que solo ensenye a pagar deuda mas rapido "
            "esta tratando el sintoma equivocado. Lo que necesita intervencion es "
            "la carga cognitiva que produce saber que se debe."
        ),
        "cifra_clave": "Deudores: +5.1% ahorro pero -2.7% satisfaccion",
        "chart": "charts/10_debt_vs_savings_satisfaction.png",
    },
    {
        "id": "F13", "subtitulo": "Hallazgo 13 -- Meta Financiera vs. Tasa de Ahorro",
        "titulo": "Ahorrar para un viaje genera mas ahorro que ahorrar para el retiro",
        "narrativa": (
            "La meta 'retiro' suena mas responsable que la meta 'viaje'. Pero quienes "
            "ahorran para un viaje tienen tasa de 10.8% -- y quienes ahorran para "
            "el retiro, solo 8.0%. Con ingresos casi identicos (~$1,020-$1,047). "
            "La mente humana responde mejor a lo concreto y cercano que a lo abstracto "
            "y lejano. El programa que empieza con retiro esta eligiendo, sin saberlo, "
            "la meta de menor efectividad comprobada."
        ),
        "cifra_clave": "10.8% tasa de ahorro (viaje) vs. 8.0% (retiro) con ingresos iguales",
        "chart": "charts/11_goal_vs_savings_rate.png",
    },
    {
        "id": "F14", "subtitulo": "Hallazgo 14 -- Gasto por Categoria en Tarjetahabientes",
        "titulo": "La tarjeta amplifica lo que eliges, no lo que debes",
        "narrativa": (
            "El gasto extra de los tarjetahabientes no esta repartido uniformemente. "
            "Se concentra en alimentacion (+16.1%) y entretenimiento (+17.2%). "
            "La vivienda apenas varia (+1.4%). La tarjeta no cambia lo que DEBEN pagar "
            "-- cambia lo que ELIGEN pagar. Y quienes la usan bien logran disfrutar mas "
            "sin comprometer su ahorro. Ese es el modulo que el programa necesita: "
            "no 'cuidado con la tarjeta', sino 'asi se usa bien'."
        ),
        "cifra_clave": "+16.1% alimentacion, +17.2% entretenimiento, +1.4% vivienda",
        "chart": "charts/12_credit_card_spending_by_category.png",
    },
    {
        "id": "AA1", "subtitulo": "Analisis Avanzado 1 -- Ahorradores Negativos",
        "titulo": "1 de cada 4 jovenes de 22 anos termina el mes en rojo",
        "narrativa": (
            "El 24.7% de los participantes de 18-22 anos gasto mas de lo que ingreso "
            "el mes encuestado. A los 29-32, ese porcentaje cae al 2.3%. No es "
            "una diferencia de caracter -- es una diferencia de anos de practica. "
            "Estos participantes no pueden absorber un modulo de ahorro antes de "
            "estabilizar su deficit mensual. El programa necesita una ruta de "
            "'emergencia primero' antes del curriculo estandar."
        ),
        "cifra_clave": "24.7% en deficit a los 18-22 vs. 2.3% a los 29-32",
        "chart": "charts/15_negative_savers_profile.png",
    },
    {
        "id": "AA2", "subtitulo": "Analisis Avanzado 2 -- Regresion OLS",
        "titulo": "Cuando controlas todo lo demas, solo dos cosas importan",
        "narrativa": (
            "El modelo OLS pone todos los factores juntos y pregunta cuanto contribuye "
            "cada uno de forma independiente. La respuesta es clara: edad (+$38 por "
            "cada 4.2 anos adicionales, p<0.001) e ingreso (+$31 por cada $377 "
            "adicionales, p<0.001). Tarjeta, IA, cuenta de ahorro, deuda: todos "
            "p > 0.60 -- sus efectos desaparecen al controlar las otras variables. "
            "El programa puede ofrecer muchas herramientas, pero solo la edad y "
            "el ingreso son predictores robustos del ahorro."
        ),
        "cifra_clave": "R2 = 0.268; solo edad e ingreso significativos (p < 0.001)",
        "chart": "charts/16_ols_coefficients.png",
    },
    {
        "id": "AA3", "subtitulo": "Analisis Avanzado 3 -- Segmentacion en 3 Perfiles",
        "titulo": "Tres tipos de participante, tres entradas distintas al programa",
        "narrativa": (
            "El algoritmo de clustering no invento categorias -- descubrio las que "
            "ya existian en los datos. 'En Riesgo' (n=170): ingreso bajo, sin deuda, "
            "sin habito. 'En Camino' (n=178): 100% con deuda, necesita gestion de metas. "
            "'Avanzado' (n=152): ingreso $1,405, IA 8h/sem, mayor satisfaccion. "
            "Estos tres perfiles requieren tres intervenciones distintas. Un curriculo "
            "unico atiende bien al promedio y mal a todos."
        ),
        "cifra_clave": "En Riesgo $809 / En Camino $884 / Avanzado $1,405 de ingreso promedio",
        "chart": "charts/17_user_clusters.png",
    },
    {
        "id": "AA4", "subtitulo": "Analisis Avanzado 4 -- Correccion FDR",
        "titulo": "Los hallazgos son solidos -- verificados con el filtro mas exigente",
        "narrativa": (
            "Cuando se hacen muchas pruebas estadisticas, aumenta el riesgo de "
            "encontrar un 'hallazgo' por puro azar. La correccion Benjamini-Hochberg "
            "ajusta los umbrales para neutralizar ese riesgo. Los cuatro hallazgos "
            "significativos del proyecto -- edad, ingreso, IA vs satisfaccion, "
            "IA vs ingreso -- sobreviven este filtro adicional. Los nulos (F7, F11, F12) "
            "estan tan lejos del umbral que ningun ajuste los moveria. Sin zona gris."
        ),
        "cifra_clave": "4/11 tests significativos despues de correccion BH; zona gris vacia",
        "chart": "charts/18_fdr_bh_correction.png",
    },
]

selected = random.choice(SPOTLIGHTS)

block = (
    "<!-- HALLAZGO_DESTACADO_START -->\n"
    "> ### Hallazgo destacado de esta corrida: {subtitulo}\n"
    ">\n"
    "> **{titulo}**\n"
    ">\n"
    "> {narrativa}\n"
    ">\n"
    "> *Cifra clave: {cifra_clave} — ver `{chart}`*\n"
    "<!-- HALLAZGO_DESTACADO_END -->"
).format(**selected)

with open("analysis-report.md", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"<!-- HALLAZGO_DESTACADO_START -->.*?<!-- HALLAZGO_DESTACADO_END -->"
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, block, content, flags=re.DOTALL)
else:
    marker = "> **Nota de transparencia:**"
    idx = content.find(marker)
    if idx != -1:
        end_idx = content.find("\n---\n", idx)
        if end_idx != -1:
            content = content[:end_idx + 5] + "\n" + block + "\n" + content[end_idx + 5:]

with open("analysis-report.md", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Hallazgo destacado: [{selected['id']}] {selected['titulo']}")
print(f"Cifra clave: {selected['cifra_clave']}")
print(f"Chart de referencia: {selected['chart']}")
