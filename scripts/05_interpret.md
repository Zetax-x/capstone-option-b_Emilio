# Phase 5 — Interpretación de Hallazgos

**Audiencia:** Directivos de Futuro Digital LatAm
**Propósito:** Traducir resultados estadísticos en insights accionables para el programa de educación financiera

---

## Hallazgo 1: Diferencias de Ingreso por País

**Los datos:** Brasil lidera la región con un ingreso mediano de $1,458 USD/mes, mientras Argentina registra el más bajo con $798 USD/mes — una brecha del 83%. Chile ($1,246) y México ($1,067) ocupan la franja media-alta; Colombia ($857) y Perú ($822) se acercan a Argentina en la franja baja. La dispersión interna también varía: Brasil tiene una desviación estándar de $592 frente a $189 de Colombia, lo que indica que Brasil concentra tanto los ingresos más altos como los más bajos de la región.

**¿Por qué importa?:** Un currículo financiero diseñado con metas en valores absolutos (ej. "ahorra $200/mes") será alcanzable para un brasileño con ingreso mediano de $1,458 pero completamente fuera de rango para un argentino ganando $766 en promedio. El riesgo no es solo de irrelevancia — es de desmotivación activa: participantes que no pueden cumplir las metas del programa tienden a abandonarlo antes de completarlo.

**Recomendación:** Calibrar todos los módulos de metas de ahorro, fondos de emergencia e inversión usando porcentajes del ingreso local, no valores en USD. Definir una tabla de referencia por país que el facilitador use para adaptar los ejercicios en tiempo real según el grupo.

**Mecanismo:** **Contexto local determina viabilidad de las metas**

**Fuente:** ingreso mediano por país — Brasil $1,458, Argentina $798 (`scripts/03_analyse.py`)

*No se encontró correlación significativa con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 2: Edad vs. Tasa de Ahorro

> 📝 *Nota metodológica — dos herramientas que aparecen en todos los hallazgos:*
>
> **¿Qué es r (coeficiente de correlación de Pearson)?**
> Mide qué tan fuertemente dos variables se mueven juntas. Va de -1 a +1. Si r = +1: cuando una variable sube, la otra siempre sube en la misma proporción — relación perfecta. Si r = -1: cuando una sube, la otra siempre baja — relación inversa perfecta. Si r = 0: no hay ningún patrón — conocer una variable no te dice nada sobre la otra. Imagínalo como puntos en un plano: r = 1 es una línea perfecta, r = 0 es una nube dispersa sin forma. En la práctica: r entre 0.1 y 0.3 es débil, entre 0.3 y 0.6 moderado, entre 0.6 y 0.8 fuerte, sobre 0.8 muy fuerte.
>
> **¿Qué es p (p-valor)?**
> Mide la probabilidad de que lo que observamos sea solo coincidencia. La pregunta exacta que responde es: "Si en realidad no hubiera ninguna relación entre estas dos variables, ¿qué tan seguido obtendríamos datos que parecieran tan relacionados como los nuestros, solo por azar?" p = 0.001 significa que solo el 0.1% de las veces — casi nunca — veríamos esto por azar: la relación es probablemente real. p = 0.50 significa que el 50% de las veces el azar produciría algo igual: no podemos distinguirlo del ruido. El umbral convencional es p < 0.05 (menos del 5% de probabilidad de que sea azar). Por encima de p = 0.10, los datos son inconcluyentes: más de 1 en 10 veces sería solo ruido.

**Los datos:** Los respondentes de 29–32 años ahorran $154 USD/mes en promedio (tasa: 16%), frente a $61 USD/mes del grupo de 18–22 años (tasa: 6%) — una brecha de 2.5x en valor absoluto y 2.7x en tasa. El ingreso promedio entre ambos grupos es prácticamente idéntico ($993 vs $1,039 USD/mes). El Finding 7 confirma estadísticamente que edad e ingreso no están relacionados en esta muestra (Pearson r = -0.029, p = 0.519): la diferencia de ahorro no puede atribuirse a que los mayores ganen más.

**¿Por qué importa?:** Si la brecha de ahorro fuera de ingreso, el programa no podría resolverla directamente — necesitaría esperar a que los participantes avancen en su carrera. Pero como es puramente conductual, el programa puede intervenir ahora: un participante de 19 años tiene exactamente el mismo potencial de ahorro que uno de 30, simplemente aún no ha formado el hábito. Esto convierte al grupo de 18–22 en el de mayor retorno de inversión para el programa.

**Recomendación:** Diseñar un módulo de formación de hábito de ahorro específico para 18–22 años, centrado en automatización: configurar una transferencia fija del 5% del ingreso el día de cobro, antes de cualquier gasto discrecional. Medir adherencia a 90 días como indicador primario del módulo, no el monto ahorrado.

**Mecanismo:** **Brecha de hábito, no de ingreso**

**Fuente:** ahorro promedio por grupo de edad y Pearson r (edad vs ingreso) = -0.029, p = 0.519 (`scripts/03_analyse.py`)

*No se encontró correlación significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 3: Desglose de Gastos por Categoría

**Los datos:** Vivienda (28.5%) y alimentación (23.8%) absorben juntas el 52.3% del ingreso mensual promedio. El entretenimiento representa apenas 8.7% y la salud 4.9%. El Finding 8 muestra que estas proporciones son notablemente estables entre los cuatro grupos de edad: vivienda oscila entre 27.5% y 29.1%, alimentación entre 23.6% y 24.1% — sin tendencia creciente ni decreciente con la edad.

**¿Por qué importa?:** El 52.3% absorbido por costos fijos deja un margen operativo limitado antes de que el ahorro siquiera entre en juego. Pero la estabilidad de las proporciones por edad (Finding 8) tiene una implicación adicional: los jóvenes de 18–22 no gastan más proporcionalmente que los de 29–32 — simplemente ahorran menos de lo que les queda. Esto refuerza la conclusión del Finding 2: el problema es de hábito, no de estructura de gasto.

**Recomendación:** Incluir un módulo de negociación de costos fijos (arrendamiento, servicios) antes de abordar el presupuesto discrecional. Dado que los gastos discrecionales representan solo el 8.7% del ingreso, las estrategias centradas en "recortar entretenimiento" tienen impacto marginal — la palanca real está en reducir o renegociar vivienda.

**Mecanismo:** **Costos fijos dominan; gastos discrecionales son palanca menor**

**Fuente:** % del ingreso por categoría y proporciones por grupo de edad (`scripts/03_analyse.py`)

**Correlación F3 × F6:** Las proporciones de vivienda del Hallazgo 3 (28.5% promedio regional) se entienden mejor desagregadas por país: Argentina (34.1%) y Chile (32.6%) tienen cargas estructuralmente más altas que Perú (24.6%). Sin embargo, la Gráfica 13 muestra que a nivel de país la correlación vivienda-ahorro es r = 0.037 porque el ingreso confunde la señal — Brasil tiene baja carga y alto ahorro porque tiene alto ingreso, no a pesar de la vivienda.

*Sin discrepancias detectadas.*

---

## Hallazgo 4: Tarjetahabientes vs. No Tarjetahabientes

**Los datos:** Los tarjetahabientes gastan 16.1% más en alimentación ($258 vs $222) y 17.2% más en entretenimiento ($95 vs $81) que quienes no tienen tarjeta, pero también ahorran 6.7% más ($101.75 vs $95.39/mes). La diferencia de ingreso entre ambos grupos es de apenas 1.5% ($1,023 vs $1,008/mes) — estadísticamente insignificante para explicar las diferencias de gasto y ahorro observadas.

**¿Por qué importa?:** El patrón desafía la narrativa de que la tarjeta de crédito daña el ahorro. Los tarjetahabientes gastan más *y* ahorran más con prácticamente el mismo ingreso, lo que sugiere un perfil de mayor involucramiento financiero general — no necesariamente de mayor disciplina, pero sí de mayor actividad. La advertencia es que sin datos sobre repago de deuda, no puede descartarse que el gasto adicional se financie con crédito revolving.

**Recomendación:** Desarrollar un módulo de crédito responsable orientado al uso como herramienta de flujo de caja: cómo liquidar el total cada mes, cómo usar la fecha de corte para extender el plazo sin costo, y cómo distinguir entre crédito como conveniencia y crédito como financiamiento de consumo. El módulo debe presentar la tarjeta como herramienta neutral — de resultado positivo o negativo dependiendo del comportamiento.

**Mecanismo:** **Involucramiento financiero activo, no ingreso, como diferenciador**

**Fuente:** ahorro y gasto promedio por tenencia de tarjeta, diferencia de ingreso +1.5% (`scripts/03_analyse.py`)

*No se encontró correlación significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 5: Uso de Herramientas de IA vs. Satisfacción Financiera

**Los datos:** Los usuarios de alto uso de IA (11+ hrs/sem, n=21) reportan satisfacción financiera promedio de 3.43/5 frente a 2.05 de los de bajo uso (0–3h/sem, n=98) — una diferencia de 1.38 puntos sobre una escala de 5. Su ingreso promedio es $1,750 vs $747 USD/mes. La correlación entre horas de IA e ingreso es r = 0.634 (p < 0.0001), más fuerte aún que la correlación con satisfacción (r = 0.571). El Finding 10 muestra que los usuarios de alto uso de IA están concentrados en el extremo superior de la distribución de ingresos dentro de cada industria — su ingreso promedio supera la mediana de su industria en 53% a 143% dependiendo del sector.

**¿Por qué importa?:** La correlación es robusta pero la causalidad es ambigua en ambas direcciones: el alto uso de IA podría causar mejores resultados financieros, o los de alto ingreso podrían tener más acceso y motivación para usar IA. El Finding 10 añade evidencia a favor de la segunda hipótesis — los usuarios de IA alta no están distribuidos aleatoriamente entre industrias, sino concentrados en los extremos superiores de cada distribución, lo que sugiere que el ingreso precede al uso de IA más que al revés.

**Recomendación:** Pilotar un módulo de alfabetización en IA financiera diseñado específicamente como experimento controlado: un grupo recibe el módulo, otro no, y se mide satisfacción financiera y comportamiento de ahorro a 6 meses. El objetivo del piloto es determinar si la adopción de IA en usuarios de ingreso bajo-medio produce mejoras medibles, o si el efecto observado es atribuible al ingreso preexistente.

**Nota de reconciliación:** El ingreso promedio de $1,750 de los usuarios de IA alta podría parecer inconsistente con las medianas por industria del Finding 9 ($915–$1,066). No hay contradicción: las medianas del Finding 9 describen al trabajador típico de cada sector. Los usuarios de IA alta no son típicos — el Finding 10 muestra visualmente que son los top earners dentro de cada industria, concentrados por encima de la mediana en todos los sectores. El promedio de $1,750 refleja que dentro de cada caja del boxplot del Finding 9, los puntos de alto uso de IA se ubican sistemáticamente en el extremo derecho.

**Mecanismo:** **Alto ingreso precede al uso intensivo de IA, no al revés**

**Fuente:** Pearson r (IA vs satisfacción) = 0.571; r (IA vs ingreso) = 0.634; comparación por industria (`scripts/03_analyse.py`)

**Correlación encontrada con Hallazgo 1:** Brasil y Chile — los países de mayor ingreso mediano — también registran los mayores promedios de uso de IA (7.1 y 6.7 hrs/sem), mientras Argentina y Colombia usan menos IA (4.2 y 4.4 hrs/sem). La brecha de acceso a herramientas digitales refuerza la brecha de ingresos entre países.

💡 *Discrepancia real: el Finding 4 muestra que tarjetahabientes ahorran más con casi el mismo ingreso (engagement financiero), y el Finding 5 muestra que usuarios de IA alta tienen más satisfacción y más ingreso — pero no hay datos que permitan confirmar si son el mismo subgrupo. Si lo son, existe un perfil unificado de "usuario financieramente activo" que el programa podría cultivar directamente. Si no lo son, son dos palancas independientes. — Sugerencia: en futuras ediciones del estudio, cruzar tenencia de tarjeta con uso de IA para identificar si el perfil se superpone.*

---

## Hallazgo 6: Carga de Vivienda por País

**Los datos:** Argentina (34.1%) y Chile (32.6%) enfrentan las cargas de vivienda más altas de la región, casi 10 puntos por encima de Perú (24.6%) que registra la más baja. Crucialmente, Argentina no es el país de menor ingreso mediano ($798) — Colombia ($857) y Perú ($822) tienen ingresos similares con cargas de vivienda de 25.4% y 24.6% respectivamente. La presión de vivienda en Argentina y Chile responde a condiciones del mercado inmobiliario, no al nivel de ingresos.

**¿Por qué importa?:** En un país donde la vivienda absorbe el 34% del ingreso, el margen disponible para todo lo demás — transporte, alimentación, educación y ahorro — es estructuralmente más estrecho. Ningún cambio de comportamiento individual puede compensar plenamente esta restricción. Un programa que aplica las mismas metas de ahorro en Argentina que en Perú está ignorando una diferencia estructural de casi 10 puntos porcentuales de ingreso disponible.

**Recomendación:** Para Argentina y Chile, complementar el currículo base con un módulo de gestión de carga de vivienda: evaluación de contratos de arrendamiento, derechos del inquilino, esquemas de vivienda asistida disponibles localmente, y estrategias de vivienda compartida. En Perú y Colombia, donde la carga es menor, diseñar un módulo que reencuadre explícitamente el margen liberado como oportunidad de ahorro — "tienes 9 puntos porcentuales más disponibles que alguien en Argentina; aquí está cómo usarlos".

**Mecanismo:** **Presión estructural de mercado independiente del comportamiento individual**

**Fuente:** carga de vivienda promedio por país — Argentina 34.1%, Perú 24.6% (`scripts/03_analyse.py`)

*No se encontró correlación significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 7 — Validación: Edad No Predice el Ingreso

**Los datos:** Pearson r (edad vs ingreso) = -0.029, p = 0.519. No existe relación estadísticamente significativa entre la edad del respondente y su ingreso mensual. Los ingresos promedio por grupo de edad son prácticamente idénticos: 18–22 años ($1,039), 23–25 ($978), 26–28 ($1,066), 29–32 ($993) — una variación máxima de $88 entre grupos, dentro del margen de error esperado para muestras de este tamaño.

> 📝 *Nota metodológica: p = 0.519 significa que, si la edad y el ingreso no tuvieran ninguna relación real entre sí, el 51.9% de las veces observaríamos un patrón igual o más extremo que el que vemos — solo por azar. Eso es más de la mitad de las veces. Cuando el azar puede explicar lo que vemos con tanta facilidad, no podemos concluir que existe una relación real. Esto no significa que la relación sea exactamente cero — significa que los datos no tienen suficiente evidencia para afirmar que existe.*

**¿Por qué importa?:** Este hallazgo de ausencia es la pieza que hace coherente el Hallazgo 2. Si los jóvenes de 18–22 ganaran significativamente menos que los de 29–32, la brecha de ahorro podría explicarse por restricción económica y el programa tendría poco margen de acción. El Hallazgo 7 cierra esa salida: los cuatro grupos de edad tienen prácticamente el mismo ingreso, lo que convierte la brecha de ahorro en un problema de hábito con solución educativa, no de acceso económico con solución de política pública.

**Recomendación:** Este hallazgo no genera un módulo propio — su función es validar la recomendación del Hallazgo 2. Permite al equipo de programa argumentar con evidencia que el módulo de ahorro automatizado para 18–22 años es la intervención de mayor retorno, porque esta población tiene capacidad económica comprobada que no está convirtiendo en ahorro.

**Mecanismo:** **La ausencia de relación como evidencia — la brecha es conductual, no económica**

**Fuente:** Pearson r = -0.029, p = 0.519; ingresos promedio por grupo de edad (`scripts/03_analyse.py`, Finding 7)

*No se encontró correlación significativa con hallazgos anteriores adicional a la validación del Hallazgo 2.*
*Sin discrepancias detectadas.*

---

## Hallazgo 8 — Validación: Proporciones de Gasto Estables por Edad

**Los datos:** Las proporciones de gasto por categoría son prácticamente idénticas entre los cuatro grupos de edad. Vivienda oscila entre 27.5% y 29.1% del ingreso; alimentación entre 23.6% y 24.1%; transporte entre 9.4% y 10.7%; entretenimiento entre 8.5% y 8.9%. Ninguna categoría muestra una tendencia sistemática creciente o decreciente con la edad.

> 📝 *Nota metodológica: "Sin tendencia sistemática" significa que si pusiéramos los cuatro grupos de edad en orden de menor a mayor, los porcentajes no suben ni bajan de forma consistente — suben y bajan de forma aleatoria, como lo haría el ruido estadístico normal entre muestras pequeñas. Es diferente a que todos los porcentajes sean exactamente iguales: la variación existe, pero no tiene dirección.*

**¿Por qué importa?:** Este hallazgo responde una hipótesis alternativa importante: si los jóvenes de 18–22 ahorraran menos porque gastan proporcionalmente más en entretenimiento o alimentación, habría justificación para un módulo de control de gastos discrecionales diferenciado por edad. Los datos refutan esta hipótesis directamente. La estructura de gasto es casi uniforme entre grupos — lo que varía no es cómo gastan sino si ahorran el margen que queda después de gastar. Esto refuerza el Hallazgo 3 y consolida la narrativa del Hallazgo 2: el problema es de hábito, no de estructura.

**Recomendación:** Al igual que el Hallazgo 7, este hallazgo valida recomendaciones existentes más que generar una nueva. Permite descartar la hipótesis de que el módulo más importante para 18–22 años es "control de gastos discrecionales". La evidencia apunta a que el módulo más efectivo es "ahorro automatizado antes de cualquier gasto", porque la distribución de gastos ya es razonablemente eficiente en todos los grupos de edad.

**Mecanismo:** **La estructura de gastos es universal; el hábito de ahorro es lo que varía con la edad**

**Fuente:** proporciones de gasto por grupo de edad — vivienda 27.5%–29.1%, entretenimiento 8.5%–8.9% (`scripts/03_analyse.py`, Finding 8)

*No se encontró correlación significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 9 — Suplementario: Ingreso por Industria

**Los datos:** Las medianas sectoriales varían entre $915 (Marketing) y $1,066 (Recursos Humanos) — una brecha de apenas $151. Sin embargo, la dispersión interna es dramática: Finanzas muestra ingresos de $300 a $2,874 dentro del mismo sector; Tecnología de $300 a $2,092; Ingeniería de $300 a $2,524. La industria elegida predice poco el ingreso mediano en etapa temprana de carrera; la posición dentro de esa industria lo predice todo.

> 📝 *Nota metodológica: "Dispersión" mide qué tan separados están los valores entre sí. Una dispersión alta significa que dentro de ese grupo hay personas con valores muy distintos. Que Finanzas tenga ingresos de $300 a $2,874 quiere decir que un analista financiero recién egresado y un director de finanzas están en el mismo grupo — sus ingresos son radicalmente distintos, aunque ambos trabajan en "Finanzas".*

**¿Por qué importa?:** Un programa que segmenta a sus participantes únicamente por industria estará agrupando perfiles financieros radicalmente distintos bajo la misma etiqueta. Diseñar módulos "para profesionales de tecnología" sin distinguir su posición en la distribución de ingresos de su sector es ignorar la variable que más impacta su capacidad de ahorro — que no es la industria sino dónde se ubican dentro de ella.

**Recomendación:** En el diagnóstico inicial del programa, además de industria y país, incluir una pregunta de posición relativa ("¿tus ingresos son más altos, similares o más bajos que los de tus colegas con la misma experiencia?"). Usar esta autoevaluación como proxy de posición dentro de la distribución sectorial para personalizar las metas de ahorro, en lugar de usar la industria como variable única de segmentación.

**Mecanismo:** **La posición dentro de la industria predice el ingreso; la industria en sí, no**

**Fuente:** medianas sectoriales $915–$1,066; dispersión interna Finanzas $300–$2,874 (`scripts/03_analyse.py`, Finding 9)

**Correlación con Hallazgo 10:** El Hallazgo 10 muestra que los usuarios de IA alta están concentrados en los extremos superiores de la distribución de cada industria. El Hallazgo 9 explica por qué esto importa: son exactamente los mismos extremos con ingresos de $2,000+ dentro de sectores con medianas de $900. Los usuarios de IA alta no son representativos de su industria — son los outliers de alto ingreso dentro de ella.

*Sin discrepancias detectadas.*

---

## Hallazgo 10 — Suplementario: Usuarios de IA Alta dentro de la Distribución de Ingreso por Industria

**Los datos:** Los 21 usuarios de alto uso de IA (11+ hrs/sem) no están distribuidos aleatoriamente entre industrias — se concentran en el extremo superior de la distribución de ingresos de cada sector. Su ingreso promedio supera la mediana de su industria en rangos que van del 53.9% (Salud) al 142.7% (Educación). Pearson r (horas IA vs ingreso) = 0.634, p < 0.0001.

**¿Por qué importa?:** El Hallazgo 5 había mostrado que usuarios de IA alta tienen mayor satisfacción e ingreso ($1,750 promedio). El Hallazgo 10 revela que este diferencial no es porque estén en industrias de mayor ingreso — es porque son los top earners dentro de cualquier industria que elijan. Esto fortalece la interpretación de que el alto ingreso precede al uso intensivo de IA (y a la satisfacción que este trae), más que al revés.

**Recomendación:** No asumir que un módulo de IA financiera por sí solo mejorará los resultados de participantes de ingreso bajo-medio. Antes de escalar ese módulo, pilotarlo como experimento controlado (ver Hallazgo 5) para distinguir si el beneficio es del módulo o del perfil de ingreso preexistente.

**Nota de reconciliación:** El ingreso promedio de $1,750 de los usuarios de IA alta (Hallazgo 5) podría parecer inconsistente con las medianas sectoriales de $915–$1,066 del Hallazgo 9. No hay contradicción: el Hallazgo 10 muestra que los usuarios de IA alta no son el trabajador típico de su sector — son los outliers de alto ingreso dentro de cada caja del boxplot, lo que explica cómo su promedio puede estar muy por encima de la mediana sectorial.

**Mecanismo:** **Alto ingreso precede al uso intensivo de IA dentro de cada industria**

**Fuente:** ingreso promedio de usuarios IA alta vs mediana sectorial — 54% a 143% por encima; r = 0.634, p < 0.0001 (`scripts/03_analyse.py`, Finding 10)

*Sin discrepancias detectadas.*

---

## Hallazgo 11: Cuenta de Ahorro vs. Comportamiento Real de Ahorro

**Los datos:** Los respondentes con cuenta de ahorro (n=362) ahorran apenas 3% más que quienes no tienen una ($100.49 vs $97.58/mes) con solo 0.5% más de ingreso ($1,018 vs $1,013/mes). La diferencia en satisfacción financiera es igualmente marginal (+3.4%). El coeficiente de Pearson entre tener cuenta de ahorro y el monto ahorrado es r = 0.014 (p = 0.760) — estadísticamente indistinguible de cero.

**¿Por qué importa?:** El 72.4% de los respondentes tiene cuenta de ahorro, lo que podría sugerir que el acceso al instrumento resuelve el problema. Los datos refutan esto directamente: tener la cuenta no predice ahorrar más. El instrumento sin el hábito es inerte. Esto contrasta con el Finding 4 donde la tarjeta de crédito sí se asocia con mayor ahorro (+6.7%) — la diferencia es que la tarjeta implica un ciclo de uso activo mensual, mientras la cuenta de ahorro puede existir sin ser utilizada.

**Recomendación:** No diseñar módulos orientados a "abrir una cuenta de ahorro" como meta en sí misma. En cambio, el módulo de ahorro debe centrarse en el comportamiento de transferencia automática — la cuenta es el contenedor, pero la transferencia programada es el hábito. La meta medible del módulo debe ser "transferencia configurada y ejecutada el primer mes", no "cuenta abierta".

**Mecanismo:** **El instrumento sin el hábito es inerte**

**Fuente:** r (cuenta_ahorro vs ahorro_mensual) = 0.014, p = 0.760 (`scripts/03_analyse.py`)

**Correlación con Hallazgo 4:** El Finding 4 muestra que tarjetahabientes ahorran 6.7% más — contrario al 3% no significativo de los cuentahabientes. Ambos son instrumentos financieros, pero la tarjeta implica uso activo mensual mientras la cuenta puede permanecer pasiva indefinidamente. Esto refuerza el mecanismo del Finding 4: es el involucramiento activo, no la tenencia del instrumento, lo que predice el ahorro.

*Sin discrepancias detectadas.*

---

## Hallazgo 12: Deuda vs. Ahorro y Satisfacción Financiera

**Los datos:** Los respondentes con deuda activa (n=234, deuda promedio $3,952) ahorran 5.1% más que quienes no tienen deuda ($101.49 vs $96.61/mes), pero reportan 2.7% menos satisfacción financiera (2.46 vs 2.53). La correlación entre tener deuda y el monto ahorrado es r = 0.026 (p = 0.564) — no significativa. Los ingresos de ambos grupos son prácticamente idénticos ($1,019 vs $1,015/mes).

**¿Por qué importa?:** La imagen popular de la deuda como enemiga del ahorro no está respaldada por estos datos: quienes tienen deuda ahorran marginalmente más, no menos. Lo que la deuda sí comprime es el bienestar percibido — la satisfacción financiera cae aunque el comportamiento de ahorro no. Esto sugiere que la deuda opera principalmente como carga psicológica, no como restricción de flujo de caja en esta muestra.

**Recomendación:** Diseñar un módulo de gestión de deuda orientado al bienestar percibido, no solo al pago: técnicas de priorización de deuda (avalancha vs bola de nieve), comunicación de progreso visible, y separación mental entre "deuda bajo control" y "deuda problemática". El objetivo no es solo reducir el saldo — es reducir la carga cognitiva que la deuda produce sobre la satisfacción financiera.

**Mecanismo:** **La deuda comprime el bienestar, no el ahorro**

**Fuente:** ahorro promedio con/sin deuda: $101.49 vs $96.61; satisfacción: 2.46 vs 2.53; r = 0.026, p = 0.564 (`scripts/03_analyse.py`)

*No se encontró correlación significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 13: Meta Financiera vs. Tasa de Ahorro Real

**Los datos:** Los respondentes cuya meta es "Ahorrar para viaje" tienen la tasa de ahorro más alta (10.8%, $112/mes), seguidos de "Fondo de emergencia" (11.0%, $107/mes) y "Comprar casa" (10.5%, $108/mes). En el extremo opuesto, "Ahorrar para retiro" registra la tasa más baja de todas (8.0%, $77/mes) y "Estudiar posgrado" la segunda más baja (8.4%, $91/mes). Los ingresos entre grupos son comparables ($941–$1,080/mes), por lo que la diferencia no se explica por capacidad económica.

**¿Por qué importa?:** El hallazgo contradice la intuición de que las metas más serias o a largo plazo generan mayor disciplina. Ocurre exactamente lo contrario: las metas concretas, cercanas y visualizables ("viaje", "casa", "emergencia") producen tasas de ahorro consistentemente más altas que las abstractas y lejanas ("retiro", "posgrado"). Un programa que empuje a jóvenes de 18–22 años a ahorrar para el retiro como primera meta está eligiendo el instrumento de menor efectividad comprobada en esta muestra.

**Recomendación:** Estructurar el módulo de metas financieras en dos niveles: primero una meta concreta de horizonte corto (3–12 meses) que genere el hábito de ahorro y la experiencia de lograrlo, y solo después introducir metas de largo plazo como el retiro. El progreso visible hacia una meta cercana es el mecanismo que sostiene el hábito — no la importancia abstracta de la meta.

**Mecanismo:** **Metas concretas y cercanas generan más ahorro que metas abstractas y lejanas**

**Fuente:** tasa de ahorro por meta financiera — retiro 8.0%, viaje 10.8% (`scripts/03_analyse.py`); gráfica `charts/11_goal_vs_savings_rate.png`

**Correlación con Hallazgo 2:** El Finding 2 identificó que los jóvenes de 18–22 ahorran menos por falta de hábito. El Finding 13 añade un mecanismo: si el programa les asigna metas de largo plazo (retiro) como primera intervención, está reforzando el patrón de bajo ahorro en lugar de romperlo. La secuencia correcta es: meta cercana → hábito → meta de largo plazo.

💡 *Discrepancia real: el Finding 13 muestra que "Pagar deudas" tiene una tasa de ahorro media (9.1%) — pero el Finding 12 muestra que tener deuda no reduce el ahorro significativamente. Esto podría indicar que quienes tienen deuda como meta ya la están gestionando activamente (y por eso ahorran a tasa normal), mientras quienes tienen deuda pero otra meta financiera son los que muestran menor bienestar. — Sugerencia: en futuras ediciones del estudio, cruzar tiene_deuda con meta_financiera para identificar si la alineación entre situación financiera real y meta declarada predice mejores resultados.*

---

## Hallazgo 14: Tarjetahabientes — Gasto Desglosado por Categoría

**Los datos:** El gasto adicional de los tarjetahabientes frente a no tarjetahabientes se concentra en dos categorías: alimentación (+16.1%, $258 vs $222/mes) y entretenimiento (+17.2%, $95 vs $81/mes). Las categorías estructurales son casi idénticas entre grupos: vivienda (+1.4%), transporte (+3.9%), salud (+4.8%). La educación muestra una diferencia media (+9.5%) que podría reflejar pagos de cursos o plataformas digitales procesados con tarjeta.

**¿Por qué importa?:** Este desglose resuelve una ambigüedad del Finding 4, que solo mostraba totales. El gasto adicional de tarjetahabientes no está distribuido uniformemente — está concentrado en las categorías más discrecionales y más susceptibles de variar mes a mes. Esto es consistente con un perfil de uso de tarjeta para consumo cotidiano (restaurantes, entretenimiento) más que para gastos estructurales. Combinado con el hecho de que también ahorran más, sugiere que la tarjeta facilita el gasto discrecional sin comprometer el ahorro — posiblemente porque el ciclo mensual de la tarjeta crea una revisión implícita del presupuesto.

**Recomendación:** En el módulo de crédito responsable, usar esta distribución como caso de enseñanza: mostrar que el gasto extra de los tarjetahabientes es discrecional (+16–17% en alimentos y entretenimiento) pero que no afecta el ahorro (+6.7%). La discusión debe centrarse en cómo distinguir cuándo el gasto discrecional con tarjeta está dentro del presupuesto vs cuándo está financiando consumo que supera el ingreso disponible.

**Mecanismo:** **El exceso de gasto con tarjeta es discrecional, no estructural**

**Fuente:** diferencia por categoría — alimentación +16.1%, entretenimiento +17.2%, vivienda +1.4% (`scripts/03_analyse.py`); gráfica `charts/12_credit_card_spending_by_category.png`

**Correlación con Hallazgo 3:** El Finding 3 muestra que entretenimiento representa solo 8.7% del ingreso promedio. El Finding 14 revela que tarjetahabientes gastan 17.2% más en esta categoría — lo que eleva su proporción a ~10.2%. Esto confirma que el gasto discrecional adicional de tarjetahabientes es real pero acotado: no redefine la estructura de gasto, solo la amplía en el margen.

*Sin discrepancias adicionales detectadas.*

---

## Gráfica 13: Carga de Vivienda vs. Ahorro Promedio por País (`charts/13_vivienda_vs_ahorro.png`)

**Los datos:** El gráfico muestra los 6 países con carga de vivienda en el eje X y ahorro mensual promedio en el eje Y. El tamaño de cada punto representa el ingreso mediano. Valores: Brasil (26.9%, $135), Chile (32.6%, $118), México (28.1%, $102), Colombia (25.4%, $82), Perú (24.6%, $81), Argentina (34.1%, $77). **Pearson r = 0.037, p = 0.944** — correlación prácticamente cero.

> 📝 *Nota metodológica — qué significan r = 0.037 y p = 0.944:*
>
> **r = 0.037** es el coeficiente de correlación de Pearson. Va de -1 a +1. Un valor de +1 significaría que cuando la carga de vivienda sube, el ahorro sube siempre en la misma proporción — relación perfecta. Un valor de -1 significaría lo opuesto: siempre baja. Un valor de 0 significaría que no hay relación: conocer la carga de vivienda de un país no te dice nada sobre su ahorro. r = 0.037 está tan cerca de cero que es prácticamente ruido — equivale a decir que la carga de vivienda explica apenas el 0.14% de la variación en ahorro entre países (r² = 0.037² ≈ 0.001, o sea, el 0.1%).
>
> **p = 0.944** es el p-valor. Responde esta pregunta: "Si no hubiera ninguna relación real entre estas dos variables, ¿qué tan probable sería obtener datos que parecieran tan correlacionados como los nuestros, solo por azar?" p = 0.944 significa que si no existiera ninguna relación real, el 94.4% de las veces — casi siempre — veríamos un patrón igual o más "correlacionado" que el nuestro, solo por variación aleatoria. En otras palabras: nuestros datos son completamente normales incluso si la relación es cero. Lo contrario de significativo.
>
> **¿Por qué no aceptamos valores con p > 0.05 (y mucho menos p > 0.10)?** La convención estadística establece que para afirmar que una relación es real y no producto del azar, el p-valor debe ser menor a 0.05 — es decir, la probabilidad de ver ese resultado por azar debería ser menor al 5%. Algunos campos aceptan hasta p < 0.10 como "resultado marginal o sugestivo" con cautela. Por encima de 0.10 (más de 1 en 10 posibilidades de que sea azar), los resultados son estadísticamente inconcluyentes: no podemos distinguir una relación real del ruido aleatorio. p = 0.944 está en el extremo opuesto — si publicáramos este resultado como hallazgo, estaríamos confundiendo ruido con señal el 94% de las veces.*

**¿Por qué importa?:** El resultado parece contradecir el Hallazgo 6, pero tiene una explicación: el ingreso confunde la relación a nivel de país. Brasil tiene la menor carga (26.9%) Y el mayor ahorro ($135) porque tiene el mayor ingreso ($1,458). Argentina tiene la mayor carga (34.1%) Y el menor ahorro ($77) porque tiene el menor ingreso ($798). Perú tiene la menor carga (24.6%) pero ahorro bajo ($81) porque su ingreso también es bajo. El ingreso domina la señal y la carga de vivienda queda enmascarada. Para aislar el efecto real de la vivienda hay que controlar el ingreso — exactamente lo que hace el OLS (AA2).

**Recomendación:** No usar esta gráfica como evidencia aislada de que "más carga → menos ahorro" — los datos de país no lo confirman (r = 0.037). Usarla en presentaciones como ilustración de por qué ingreso y vivienda deben analizarse conjuntamente, remitiendo al OLS (AA2) como la herramienta que los separa correctamente.

**Mecanismo:** **El ingreso enmascara el efecto de la vivienda cuando se analiza a nivel de país**

**Fuente:** r = 0.037, p = 0.944 (`scripts/06_correlations.py`, `charts/13_vivienda_vs_ahorro.png`)

**Correlación G13 × F1 y F6:** Esta gráfica integra F1 (ingreso por país, visible en tamaño del punto) y F6 (carga de vivienda). La ausencia de correlación (r = 0.037) es en sí misma el hallazgo: el ingreso confunde la relación vivienda-ahorro a nivel agregado.

💡 *Discrepancia real: El Hallazgo 6 implica que mayor carga de vivienda reduce el margen de ahorro, pero la Gráfica 13 muestra r = 0.037 — Chile (carga 32.6%) ahorra $118 mientras Perú (carga 24.6%) ahorra solo $81. El mecanismo es que el ingreso domina sobre la vivienda al comparar países. Sugerencia: presentar siempre G13 junto al OLS (AA2) que controla por ingreso y aísla el efecto real de la vivienda.*

---

## Gráfica 14: Uso de IA vs. Satisfacción Financiera por País (`charts/14_ia_vs_satisfaccion.png`)

**Los datos:** Valores por país: Brasil (7.1 hrs, satisfacción 2.83), Chile (6.7 hrs, 2.71), México (5.5 hrs, 2.50), Perú (4.7 hrs, 2.32), Colombia (4.4 hrs, 2.33), Argentina (4.2 hrs, 2.20). **Pearson r = 0.992, p = 0.000** — correlación casi perfecta y estadísticamente significativa incluso con n=6, superando el umbral r > 0.81 requerido. El patrón individual (F5: r = 0.571) y el patrón de país (r = 0.992) van en la misma dirección.

> 📝 *Nota metodológica — qué significa r = 0.992 y por qué p = 0.000 aquí sí es válido:*
>
> **r = 0.992** significa correlación casi perfecta. Para tener una referencia: r = 0.5 es una relación moderada; r = 0.7 es fuerte; r = 0.9 es muy fuerte; r = 0.992 es prácticamente una línea recta. Si graficáramos uso de IA vs. satisfacción para los 6 países, los puntos caerían casi exactamente sobre una línea. El 98.4% de la variación en satisfacción entre países queda explicada por el uso de IA (r² = 0.992² ≈ 0.984).
>
> **p = 0.000** aquí es válido, a diferencia de la Gráfica 13. Con n=6 países, normalmente se necesita r > 0.81 para alcanzar p < 0.05 — y r = 0.992 lo supera por amplio margen. La razón por la que esta correlación "pasa el filtro" con solo 6 puntos es precisamente porque es tan extrema (0.992) que sería casi imposible obtenerla por azar si no hubiera ninguna relación real.
>
> **La advertencia importante:** p = 0.000 confirma que la correlación no es azar, pero no confirma que el uso de IA *cause* la satisfacción. Puede ser que un tercer factor — el ingreso — esté causando ambas cosas simultáneamente: los países más ricos (Brasil, Chile) tienen más dinero para comprar herramientas digitales Y más razones para estar satisfechos financieramente. La correlación es real; la causalidad no está demostrada.*

**¿Por qué importa?:** Esta es la única correlación del proyecto que es significativa tanto a nivel individual (F5: r = 0.571) como a nivel de país (r = 0.992). La consistencia entre dos niveles de análisis distintos fortalece la asociación — pero el ingreso sigue siendo el confundidor principal. Los países más ricos (Brasil, Chile) usan más IA y tienen mayor satisfacción; los más pobres (Argentina, Colombia) usan menos y tienen menor satisfacción. La correlación puede ser real, puede ser espuria, o puede ser ambas cosas simultáneamente a distintas escalas.

**Recomendación:** Presentar G14 junto a F5 como evidencia de consistencia multi-nivel: "el patrón IA-satisfacción existe tanto entre individuos como entre países". Siempre acompañarla del OLS (AA2) que muestra que el efecto de la IA sobre el ahorro desaparece al controlar el ingreso — la asociación es consistente pero la causalidad no está demostrada.

**Mecanismo:** **Uso de IA y satisfacción co-varían a nivel de país, mediados por el ingreso**

**Fuente:** r = 0.992, p = 0.000 (`scripts/06_correlations.py`, `charts/14_ia_vs_satisfaccion.png`)

**Correlación G14 × F5 y F1:** El patrón país-nivel (G14) es consistente con el patrón individual (F5: r = 0.571). F1 añade el contexto: los países de mayor ingreso son los de mayor uso de IA y mayor satisfacción, sugiriendo que el ingreso es la variable mediadora en ambos niveles de análisis.

💡 *Discrepancia real: La Gráfica 14 muestra r = 0.992 a nivel de país, pero el OLS (AA2) muestra que el efecto de la IA sobre el ahorro no es significativo cuando se controla el ingreso (p = 0.657). Los dos análisis no se contradicen — uno mide satisfacción y el otro ahorro, y operan a distintos niveles — pero un lector no técnico podría leer "IA predice satisfacción perfectamente" y "IA no predice ahorro" como contradicción. Sugerencia: presentar siempre G14 y OLS juntos con nota explícita de que miden variables y niveles distintos.*

---

## Análisis Avanzado 1: Perfil de Ahorradores Negativos (`charts/15_negative_savers_profile.png`)

**Los datos:** 74 de los 500 participantes (14.8%) reportaron ahorro mensual negativo en el período encuestado — es decir, gastaron más de lo que ingresaron ese mes. La concentración por edad es clara: el 24.7% del grupo de 18–22 años tiene ahorro negativo, frente a apenas el 2.3% del grupo de 29–32. La distribución por país muestra que Perú (20.0%), Colombia (18.8%) y Brasil (15.4%) tienen las proporciones más altas. El perfil de este subgrupo muestra ingresos ligeramente menores que los ahorradores positivos ($918 vs $1,034), mayor uso de tarjeta de crédito y niveles similares de deuda activa.

> 📝 *Nota metodológica: "Ahorro negativo" no significa que alguien perdió dinero de sus ahorros acumulados. Significa que en el mes encuestado gastó más de lo que ingresó — lo que puede ocurrir por usar crédito, tomar dinero de ahorros previos, o recibir apoyo de terceros. Es como cuando uno "va en rojo" ese mes. No dice nada sobre su situación financiera histórica, solo sobre ese período.*

**¿Por qué importa?:** Este subgrupo representa casi 1 de cada 6 participantes y es el de mayor urgencia del programa — pero es también el más difícil de retener, porque quienes están en crisis financiera inmediata tienen menor capacidad de atención para módulos educativos. El hecho de que el 24.7% de los jóvenes de 18–22 esté en esta situación, frente al 2.3% de los de 29–32, refuerza que el problema no es estructural sino de etapa de vida: los participantes de más edad han salido de esta zona por acumulación de experiencia y hábito, no por mayor ingreso (Hallazgo 7).

**Recomendación:** Crear un módulo de "estabilización de emergencia" específico para el subgrupo de ahorro negativo, separado del currículo base. Este módulo debe tener horizonte de 30–60 días y metas mínimas alcanzables (reducir el déficit mensual, no alcanzar ahorro positivo de inmediato). Identificar a estos participantes en el diagnóstico inicial y derivarlos a esta ruta antes de cualquier otro módulo.

**Mecanismo:** **Déficit mensual como estado transitorio de etapa de vida, no como condición estructural permanente**

**Fuente:** 74/500 participantes con ahorro negativo; concentración en 18–22 años: 24.7% vs 29–32: 2.3% (`scripts/07_advanced.py`, Sección 1)

**Correlación con Hallazgos 2 y 6:** El Hallazgo 2 muestra que los jóvenes de 18–22 ahorran menos en general. El Análisis Avanzado 1 revela que dentro de ese grupo, una cuarta parte está en déficit — no solo en ahorro bajo. El Hallazgo 6 (carga de vivienda) puede ser un factor agravante para los ahorradores negativos, cuya carga de vivienda (27.4%) es comparable a la del resto de la muestra pero combinada con menor ingreso produce déficit más fácilmente.

*Sin discrepancias detectadas.*

---

## Análisis Avanzado 2: Regresión OLS — ¿Qué Predice el Ahorro? (`charts/16_ols_coefficients.png`)

**Los datos:** La regresión OLS con 6 predictores explica el 26.8% de la varianza en el ahorro mensual (R² = 0.268). El error promedio del modelo es $82.31 USD (RMSE). Solo dos variables son estadísticamente significativas: edad (+$38.16 USD por cada desviación estándar de edad, equivalente a ~4.2 años; p < 0.001) e ingreso mensual (+$31.45 USD por desviación estándar; p < 0.001). Las cuatro variables restantes — uso de IA, tarjeta de crédito, cuenta de ahorro y deuda activa — no tienen efecto significativo independiente (todos p > 0.60) cuando se controlan la edad y el ingreso.

> 📝 *Nota metodológica: Una regresión OLS (Mínimos Cuadrados Ordinarios) hace algo que los análisis individuales de los Hallazgos 1–14 no podían hacer: ver el efecto de cada variable mientras mantiene las demás constantes. Es como comparar dos personas idénticas en todo — misma edad, mismo ingreso, mismo país — excepto en que una tiene tarjeta de crédito y la otra no. La regresión pregunta: en esa comparación, ¿la tarjeta predice más ahorro? Si la respuesta es "no" (p alto), el efecto que habíamos visto en el Hallazgo 4 probablemente ocurría porque los tarjetahabientes también tenían mayores ingresos o edades — no por la tarjeta en sí. "Desviación estándar" es una forma de medir cuánto varía algo. Decir que la edad sube $38 por SD significa que pasar de ser "joven promedio" a "algo mayor que el promedio" predice $38 más de ahorro mensual.*

**¿Por qué importa?:** Este análisis es el test más riguroso del proyecto. Cuando se controla por todo lo demás, el resultado es contundente: la edad y el ingreso son los dos únicos predictores robustos del ahorro. Los instrumentos financieros — tarjeta, cuenta de ahorro, uso de IA, deuda — pierden su poder predictivo cuando se les compara dentro del mismo perfil de edad e ingreso. Esto confirma el mecanismo central del Hallazgo 11 desde un ángulo completamente diferente: el instrumento sin el hábito es inerte.

**Recomendación:** Usar estos resultados para priorizar el currículo: invertir primero en el hábito de ahorro (edad como proxy de acumulación de experiencia) y en estrategias de crecimiento de ingreso dentro de la industria (Hallazgo 9). Los módulos de instrumentos financieros (tarjeta, IA, cuenta) tienen valor educativo pero no deben presentarse como predictores independientes de mayor ahorro — los datos muestran que su efecto, cuando se aísla, no es estadísticamente distinguible de cero.

**Mecanismo:** **Edad e ingreso como únicos predictores robustos del ahorro; los instrumentos son neutros en igualdad de condiciones**

**Fuente:** R² = 0.268, RMSE = $82.31, N = 500; coeficientes edad +$38.16 p<0.001, ingreso +$31.45 p<0.001 (`scripts/07_advanced.py`, Sección 2)

**Correlación con Hallazgos 4, 5 y 11:** El OLS reconcilia tres hallazgos aparentemente contradictorios. El Hallazgo 4 mostraba que tarjetahabientes ahorran más (+6.7%) y el Hallazgo 5 que usuarios de IA alta también. El Hallazgo 11 ya sugería que la cuenta de ahorro no predice nada. El OLS unifica los tres: ningún instrumento tiene efecto independiente. Las diferencias de los Hallazgos 4 y 5 ocurrían porque esos grupos tenían perfiles de edad e ingreso ligeramente distintos.

*Sin discrepancias detectadas.*

---

## Análisis Avanzado 3: Segmentación — Tres Perfiles de Usuario (`charts/17_user_clusters.png`)

**Los datos:** El algoritmo de clustering identificó tres grupos naturales en los datos, diferenciados principalmente por ingreso, presencia de deuda y uso de IA. "En Riesgo" (n=170): ingreso $809, ahorro $75, satisfacción 2.20, sin deuda activa. "En Camino" (n=178): ingreso $884, ahorro $85, satisfacción 2.26, 100% con deuda activa. "Avanzado" (n=152): ingreso $1,405, ahorro $142, satisfacción 3.05, 37% con deuda, 8 hrs/sem de IA frente a 3.9–4.6 de los otros grupos.

> 📝 *Nota metodológica: El clustering (o segmentación) es un algoritmo que agrupa a las personas en categorías basándose en su similitud — sin que el analista defina las categorías de antemano. Es como dejar que los datos mismos encuentren sus propios grupos naturales. El gráfico radar (o de araña) que acompaña este análisis muestra cada grupo como un polígono: los ejes son las variables financieras, y cuanto más grande es el polígono en un eje, más alto es ese grupo en esa dimensión. Si un polígono es mucho más grande que otro en "ingreso", ese grupo tiene más ingresos.*

**¿Por qué importa?:** Los tres perfiles son cualitativamente distintos y requieren intervenciones distintas. "En Riesgo" no tiene deuda — su restricción es el ingreso bajo combinado con ausencia de hábito. "En Camino" tiene deuda al 100% y satisfacción apenas superior — responde al módulo de gestión de deuda y concreción de metas. "Avanzado" muestra el perfil objetivo: más ingreso, más ahorro, más uso de IA, mayor satisfacción. La distancia entre "En Riesgo" y "Avanzado" es la brecha que el programa debe cerrar, y la segmentación permite diseñar la ruta de cada punto de partida.

**Recomendación:** Incorporar el diagnóstico de perfil al inicio del programa. Un cuestionario de 5 preguntas (ingreso, ahorro actual, deuda activa, uso de IA, satisfacción autorreportada) permite asignar a cada participante a uno de los tres perfiles y derivarlos al módulo de entrada correspondiente. No usar un currículo único: los tres perfiles requieren énfasis distintos (ingreso y hábito para "En Riesgo", deuda y metas para "En Camino", consolidación y herramientas para "Avanzado").

**Mecanismo:** **Tres rutas de entrada al programa según el perfil financiero inicial**

**Fuente:** k-means k=3; perfiles: En Riesgo n=170 $809, En Camino n=178 $884, Avanzado n=152 $1,405 (`scripts/07_advanced.py`, Sección 3)

**Correlación con Hallazgos 2, 12 y 13:** El perfil "En Camino" (100% deuda) corresponde al subgrupo del Hallazgo 12 que tiene menor satisfacción pese a mayor ingreso. El perfil "En Riesgo" corresponde al extremo joven del Hallazgo 2. La meta de "Invertir en bolsa" del grupo "Avanzado" confirma el Hallazgo 13: quienes ya tienen hábito de ahorro eligen metas de mayor complejidad.

*Sin discrepancias detectadas.*

---

## Análisis Avanzado 4: Robustez Estadística — Corrección FDR Benjamini-Hochberg (`charts/18_fdr_bh_correction.png`)

**Los datos:** 11 tests estadísticos formales del proyecto (5 correlaciones de Pearson + 6 coeficientes de la regresión OLS) fueron evaluados con corrección Benjamini-Hochberg al nivel FDR = 0.05. Resultados: 4 tests sobreviven la corrección — OLS: Edad (p < 0.001), OLS: Ingreso (p < 0.001), F5: IA vs satisfacción (p = 0.0001), F10: IA vs ingreso (p = 0.0001). Los 7 tests restantes no son significativos y la corrección no cambia su estatus. No hay ningún test en la "zona gris" de p = 0.01–0.10.

> 📝 *Nota metodológica: Cuando hacemos muchas pruebas estadísticas sobre los mismos datos, aumenta la probabilidad de que alguna salga "significativa" solo por azar — como lanzar una moneda 11 veces: es probable que salga cara varias veces seguidas aunque la moneda sea justa. La corrección de Benjamini-Hochberg (BH) ajusta los umbrales de significancia para tener en cuenta este problema. Un hallazgo que "sobrevive" la corrección BH es más confiable que uno que solo pasó el umbral estándar. La "zona gris" son los tests con p entre 0.01 y 0.10 — suficientemente bajos para parecer interesantes, pero suficientemente altos para poder ser falsos positivos. Si hay tests en esa zona, la corrección BH puede cambiar su conclusión. En este proyecto, no hay ninguno.*

**¿Por qué importa?:** Este análisis es la garantía de calidad estadística del proyecto. Confirma que los dos hallazgos significativos principales (IA vs satisfacción, IA vs ingreso) no son artefactos de haber corrido muchas pruebas — sobreviven el test más exigente disponible. Los hallazgos no significativos (F7, F11, F12) estaban tan lejos del umbral que la corrección no cambia nada. La zona gris está vacía, lo que significa que no hay resultados en riesgo de ser malinterpretados.

**Recomendación:** Incluir la tabla de corrección BH en el apéndice metodológico del informe ejecutivo cuando se presente al consejo directivo. Los hallazgos de este proyecto pueden presentarse con confianza estadística completa: los significativos son robustos y los no significativos están claramente por encima del umbral.

**Mecanismo:** **Validación cruzada estadística: los hallazgos significativos sobreviven el test más exigente**

**Fuente:** 11 tests evaluados; 4/11 significativos después de corrección BH (`scripts/07_advanced.py`, Sección 4)

**Correlación con todos los hallazgos anteriores:** Este análisis es el cierre metodológico del proyecto. Valida que F5 y F10 (los dos hallazgos de IA) son robustos, y confirma que F7, F11 y F12 son genuinamente nulos — no son hallazgos débiles que una corrección podría rescatar, sino ausencias de relación bien establecidas.

*Sin discrepancias detectadas.*

---

## Conclusión General

**1. La brecha de ahorro es de hábito, el instrumento es neutro sin él, y la meta lo activa o lo suprime**

Los Hallazgos 2, 7 y 8 convergen en una sola conclusión, confirmada visualmente en `charts/19_savings_rate_vs_income_by_age.png`: los jóvenes de 18–22 no ahorran menos porque ganen menos (r = -0.029, p = 0.519, F7) ni porque gasten más proporcionalmente (F8) — la tasa de ahorro sube de 6% a 16% mientras el ingreso se mantiene plano. El Análisis Avanzado 2 (OLS) añade el nivel más riguroso de evidencia: cuando se controla por edad e ingreso, ningún instrumento financiero — tarjeta, cuenta de ahorro, IA, deuda — tiene efecto independiente sobre el ahorro (todos p > 0.60). El instrumento sin el hábito es inerte (F11, validado por dos métodos independientes). Y el Hallazgo 13 cierra el argumento con el dato más contraintuitivo del proyecto: los que ahorran para el retiro tienen la tasa más baja (8.0%), mientras los que ahorran para un viaje tienen la más alta (10.8%) — la concreción de la meta activa el hábito, su abstracción lo suprime.

**2. El involucramiento activo predice resultados, pero el ingreso es el confundidor en todos los niveles**

Los Hallazgos 4, 5, 10, 14 y la Gráfica 14 revelan que el involucramiento activo produce mejores resultados — pero el ingreso subyace en todos los casos. La Gráfica 14 muestra r = 0.992 entre uso de IA y satisfacción a nivel de país (estadísticamente significativo con n=6), consistente con el F5 individual (r = 0.571) — la misma dirección en dos niveles de análisis distintos fortalece la asociación. Sin embargo, el F10 muestra que los usuarios de IA alta son top earners dentro de su industria, y el OLS (AA2) confirma que el efecto de la IA desaparece al controlar el ingreso (p = 0.657). La Gráfica 13 añade el contrapunto: la correlación vivienda-ahorro a nivel de país es r = 0.037 — también porque el ingreso enmascara la señal. El ingreso es el confundidor estructural del proyecto en ambas correlaciones cruzadas. El involucramiento activo importa, pero distinguir cuánto es del instrumento y cuánto del perfil económico del participante requiere el experimento controlado del F5.

**3. Las brechas entre países son estructurales y no pueden resolverse solo con módulos conductuales**

Los Hallazgos 1, 6 y la Gráfica 13 muestran que Argentina y Chile tienen cargas de vivienda de 32–34% frente al 24–25% de Perú y Colombia. El Análisis Avanzado 1 añade que el 14.8% de los participantes está en déficit mensual, con concentración en países de ingreso medio-bajo. El OLS confirma que el ingreso es el segundo predictor más fuerte del ahorro (+$31.45/SD). Esta combinación — alta presión estructural de vivienda + menor ingreso — crea un techo de ahorro que ningún cambio conductual puede superar completamente. El Hallazgo 9 complica aún más el cuadro: dentro de cada país e industria, la posición en la distribución de ingresos predice más que la industria en sí. Un currículo uniforme no puede atender estas realidades divergentes: se requiere calibración por país, por perfil de usuario (Análisis Avanzado 3) y por posición en la distribución de ingresos.

**4. La segmentación en tres perfiles transforma el programa de un currículo único a tres rutas de entrada**

El Análisis Avanzado 3 produce la implicación más accionable del proyecto: los 500 participantes se agrupan naturalmente en tres perfiles con necesidades radicalmente distintas — "En Riesgo" (n=170, sin deuda, ingreso bajo, sin hábito), "En Camino" (n=178, 100% con deuda, ingreso medio, hábito parcial), "Avanzado" (n=152, mayor ingreso, mayor uso de IA, mayor satisfacción). La distancia entre "En Riesgo" y "Avanzado" es exactamente la brecha que el programa debe cerrar. El Análisis Avanzado 4 (FDR) garantiza que los 4 hallazgos estadísticamente significativos del proyecto (edad, ingreso, IA-satisfacción, IA-ingreso) son robustos y pueden presentarse con confianza al consejo directivo. Las discrepancias abiertas (perfil unificado de usuario activo, relación deuda-meta-ahorro) son preguntas de investigación para la siguiente edición del estudio, no debilidades del análisis actual.

**Recomendación prioritaria**

El mayor impacto del programa se logrará en tres pasos secuenciados. Primero, implementar diagnóstico de perfil al inicio (5 preguntas) para asignar a cada participante a una de las tres rutas del Análisis Avanzado 3. Segundo, para el perfil "En Riesgo" (y especialmente para jóvenes de 18–22 años en Argentina y Chile), arrancar con el módulo de estabilización de emergencia (Análisis Avanzado 1) antes del currículo base — no tiene sentido enseñar ahorro programado a alguien que termina cada mes en déficit. Tercero, en todos los perfiles, estructurar las metas financieras en horizonte corto primero (Hallazgo 13), con transferencia automática configurada desde el primer sueldo (Hallazgo 2), y retroalimentación mensual visible del progreso. Este trío — diagnóstico → estabilización → hábito con meta concreta — ataca simultáneamente la brecha conductual (H2, H7, H8, H11), la crisis de subgrupo vulnerable (AA1) y el mecanismo de activación del ahorro (H13), con evidencia estadística robusta respaldada por corrección FDR (AA4) en cada paso.
