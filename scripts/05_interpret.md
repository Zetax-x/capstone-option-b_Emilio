# Phase 5 â€” InterpretaciÃ³n de Hallazgos

**Audiencia:** Directivos de Futuro Digital LatAm
**PropÃ³sito:** Traducir resultados estadÃ­sticos en insights accionables para el programa de educaciÃ³n financiera

---

## Hallazgo 1: Diferencias de Ingreso por PaÃ­s

**Los datos:** Brasil lidera la regiÃ³n con un ingreso mediano de $1,458 USD/mes, mientras Argentina registra el mÃ¡s bajo con $798 USD/mes â€” una brecha del 83%. Chile ($1,246) y MÃ©xico ($1,067) ocupan la franja media-alta; Colombia ($857) y PerÃº ($822) se acercan a Argentina en la franja baja. La dispersiÃ³n interna tambiÃ©n varÃ­a: Brasil tiene una desviaciÃ³n estÃ¡ndar de $592 frente a $189 de Colombia, lo que indica que Brasil concentra tanto los ingresos mÃ¡s altos como los mÃ¡s bajos de la regiÃ³n.

**Â¿Por quÃ© importa?:** Un currÃ­culo financiero diseÃ±ado con metas en valores absolutos (ej. "ahorra $200/mes") serÃ¡ alcanzable para un brasileÃ±o con ingreso mediano de $1,458 pero completamente fuera de rango para un argentino ganando $766 en promedio. El riesgo no es solo de irrelevancia â€” es de desmotivaciÃ³n activa: participantes que no pueden cumplir las metas del programa tienden a abandonarlo antes de completarlo.

**RecomendaciÃ³n:** Calibrar todos los mÃ³dulos de metas de ahorro, fondos de emergencia e inversiÃ³n usando porcentajes del ingreso local, no valores en USD. Definir una tabla de referencia por paÃ­s que el facilitador use para adaptar los ejercicios en tiempo real segÃºn el grupo.

**Mecanismo:** **Contexto local determina viabilidad de las metas**

**Fuente:** ingreso mediano por paÃ­s â€” Brasil $1,458, Argentina $798 (`scripts/03_analyse.py`)

*No se encontrÃ³ correlaciÃ³n significativa con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 2: Edad vs. Tasa de Ahorro

> ðŸ“ *Nota metodolÃ³gica â€” dos herramientas que aparecen en todos los hallazgos:*
>
> **Â¿QuÃ© es r (coeficiente de correlaciÃ³n de Pearson)?**
> Mide quÃ© tan fuertemente dos variables se mueven juntas. Va de -1 a +1. Si r = +1: cuando una variable sube, la otra siempre sube en la misma proporciÃ³n â€” relaciÃ³n perfecta. Si r = -1: cuando una sube, la otra siempre baja â€” relaciÃ³n inversa perfecta. Si r = 0: no hay ningÃºn patrÃ³n â€” conocer una variable no te dice nada sobre la otra. ImagÃ­nalo como puntos en un plano: r = 1 es una lÃ­nea perfecta, r = 0 es una nube dispersa sin forma. En la prÃ¡ctica: r entre 0.1 y 0.3 es dÃ©bil, entre 0.3 y 0.6 moderado, entre 0.6 y 0.8 fuerte, sobre 0.8 muy fuerte.
>
> **Â¿QuÃ© es p (p-valor)?**
> Mide la probabilidad de que lo que observamos sea solo coincidencia. La pregunta exacta que responde es: "Si en realidad no hubiera ninguna relaciÃ³n entre estas dos variables, Â¿quÃ© tan seguido obtendrÃ­amos datos que parecieran tan relacionados como los nuestros, solo por azar?" p = 0.001 significa que solo el 0.1% de las veces â€” casi nunca â€” verÃ­amos esto por azar: la relaciÃ³n es probablemente real. p = 0.50 significa que el 50% de las veces el azar producirÃ­a algo igual: no podemos distinguirlo del ruido. El umbral convencional es p < 0.05 (menos del 5% de probabilidad de que sea azar). Por encima de p = 0.10, los datos son inconcluyentes: mÃ¡s de 1 en 10 veces serÃ­a solo ruido.

**Los datos:** Los respondentes de 29â€“32 aÃ±os ahorran $154 USD/mes en promedio (tasa: 16%), frente a $61 USD/mes del grupo de 18â€“22 aÃ±os (tasa: 6%) â€” una brecha de 2.5x en valor absoluto y 2.7x en tasa. El ingreso promedio entre ambos grupos es prÃ¡cticamente idÃ©ntico ($993 vs $1,039 USD/mes). El Finding 7 confirma estadÃ­sticamente que edad e ingreso no estÃ¡n relacionados en esta muestra (Pearson r = -0.029, p = 0.519): la diferencia de ahorro no puede atribuirse a que los mayores ganen mÃ¡s.

**Â¿Por quÃ© importa?:** Si la brecha de ahorro fuera de ingreso, el programa no podrÃ­a resolverla directamente â€” necesitarÃ­a esperar a que los participantes avancen en su carrera. Pero como es puramente conductual, el programa puede intervenir ahora: un participante de 19 aÃ±os tiene exactamente el mismo potencial de ahorro que uno de 30, simplemente aÃºn no ha formado el hÃ¡bito. Esto convierte al grupo de 18â€“22 en el de mayor retorno de inversiÃ³n para el programa.

**RecomendaciÃ³n:** DiseÃ±ar un mÃ³dulo de formaciÃ³n de hÃ¡bito de ahorro especÃ­fico para 18â€“22 aÃ±os, centrado en automatizaciÃ³n: configurar una transferencia fija del 5% del ingreso el dÃ­a de cobro, antes de cualquier gasto discrecional. Medir adherencia a 90 dÃ­as como indicador primario del mÃ³dulo, no el monto ahorrado.

**Mecanismo:** **Brecha de hÃ¡bito, no de ingreso**

**Fuente:** ahorro promedio por grupo de edad y Pearson r (edad vs ingreso) = -0.029, p = 0.519 (`scripts/03_analyse.py`)

*No se encontrÃ³ correlaciÃ³n significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 3: Desglose de Gastos por CategorÃ­a

**Los datos:** Vivienda (28.5%) y alimentaciÃ³n (23.8%) absorben juntas el 52.3% del ingreso mensual promedio. El entretenimiento representa apenas 8.7% y la salud 4.9%. El Finding 8 muestra que estas proporciones son notablemente estables entre los cuatro grupos de edad: vivienda oscila entre 27.5% y 29.1%, alimentaciÃ³n entre 23.6% y 24.1% â€” sin tendencia creciente ni decreciente con la edad.

**Â¿Por quÃ© importa?:** El 52.3% absorbido por costos fijos deja un margen operativo limitado antes de que el ahorro siquiera entre en juego. Pero la estabilidad de las proporciones por edad (Finding 8) tiene una implicaciÃ³n adicional: los jÃ³venes de 18â€“22 no gastan mÃ¡s proporcionalmente que los de 29â€“32 â€” simplemente ahorran menos de lo que les queda. Esto refuerza la conclusiÃ³n del Finding 2: el problema es de hÃ¡bito, no de estructura de gasto.

**RecomendaciÃ³n:** Incluir un mÃ³dulo de negociaciÃ³n de costos fijos (arrendamiento, servicios) antes de abordar el presupuesto discrecional. Dado que los gastos discrecionales representan solo el 8.7% del ingreso, las estrategias centradas en "recortar entretenimiento" tienen impacto marginal â€” la palanca real estÃ¡ en reducir o renegociar vivienda.

**Mecanismo:** **Costos fijos dominan; gastos discrecionales son palanca menor**

**Fuente:** % del ingreso por categorÃ­a y proporciones por grupo de edad (`scripts/03_analyse.py`)

**CorrelaciÃ³n F3 Ã— F6:** Las proporciones de vivienda del Hallazgo 3 (28.5% promedio regional) se entienden mejor desagregadas por paÃ­s: Argentina (34.1%) y Chile (32.6%) tienen cargas estructuralmente mÃ¡s altas que PerÃº (24.6%). Sin embargo, la GrÃ¡fica 13 muestra que a nivel de paÃ­s la correlaciÃ³n vivienda-ahorro es r = 0.037 porque el ingreso confunde la seÃ±al â€” Brasil tiene baja carga y alto ahorro porque tiene alto ingreso, no a pesar de la vivienda.

*Sin discrepancias detectadas.*

---

## Hallazgo 4: Tarjetahabientes vs. No Tarjetahabientes

**Los datos:** Los tarjetahabientes gastan 16.1% mÃ¡s en alimentaciÃ³n ($258 vs $222) y 17.2% mÃ¡s en entretenimiento ($95 vs $81) que quienes no tienen tarjeta, pero tambiÃ©n ahorran 6.7% mÃ¡s ($101.75 vs $95.39/mes). La diferencia de ingreso entre ambos grupos es de apenas 1.5% ($1,023 vs $1,008/mes) â€” estadÃ­sticamente insignificante para explicar las diferencias de gasto y ahorro observadas.

**Â¿Por quÃ© importa?:** El patrÃ³n desafÃ­a la narrativa de que la tarjeta de crÃ©dito daÃ±a el ahorro. Los tarjetahabientes gastan mÃ¡s *y* ahorran mÃ¡s con prÃ¡cticamente el mismo ingreso, lo que sugiere un perfil de mayor involucramiento financiero general â€” no necesariamente de mayor disciplina, pero sÃ­ de mayor actividad. La advertencia es que sin datos sobre repago de deuda, no puede descartarse que el gasto adicional se financie con crÃ©dito revolving.

**RecomendaciÃ³n:** Desarrollar un mÃ³dulo de crÃ©dito responsable orientado al uso como herramienta de flujo de caja: cÃ³mo liquidar el total cada mes, cÃ³mo usar la fecha de corte para extender el plazo sin costo, y cÃ³mo distinguir entre crÃ©dito como conveniencia y crÃ©dito como financiamiento de consumo. El mÃ³dulo debe presentar la tarjeta como herramienta neutral â€” de resultado positivo o negativo dependiendo del comportamiento.

**Mecanismo:** **Involucramiento financiero activo, no ingreso, como diferenciador**

**Fuente:** ahorro y gasto promedio por tenencia de tarjeta, diferencia de ingreso +1.5% (`scripts/03_analyse.py`)

*No se encontrÃ³ correlaciÃ³n significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 5: Uso de Herramientas de IA vs. SatisfacciÃ³n Financiera

**Los datos:** Los usuarios de alto uso de IA (11+ hrs/sem, n=21) reportan satisfacciÃ³n financiera promedio de 3.43/5 frente a 2.05 de los de bajo uso (0â€“3h/sem, n=98) â€” una diferencia de 1.38 puntos sobre una escala de 5. Su ingreso promedio es $1,750 vs $747 USD/mes. La correlaciÃ³n entre horas de IA e ingreso es r = 0.634 (p < 0.0001), mÃ¡s fuerte aÃºn que la correlaciÃ³n con satisfacciÃ³n (r = 0.571). El Finding 10 muestra que los usuarios de alto uso de IA estÃ¡n concentrados en el extremo superior de la distribuciÃ³n de ingresos dentro de cada industria â€” su ingreso promedio supera la mediana de su industria en 53% a 143% dependiendo del sector.

**Â¿Por quÃ© importa?:** La correlaciÃ³n es robusta pero la causalidad es ambigua en ambas direcciones: el alto uso de IA podrÃ­a causar mejores resultados financieros, o los de alto ingreso podrÃ­an tener mÃ¡s acceso y motivaciÃ³n para usar IA. El Finding 10 aÃ±ade evidencia a favor de la segunda hipÃ³tesis â€” los usuarios de IA alta no estÃ¡n distribuidos aleatoriamente entre industrias, sino concentrados en los extremos superiores de cada distribuciÃ³n, lo que sugiere que el ingreso precede al uso de IA mÃ¡s que al revÃ©s.

**RecomendaciÃ³n:** Pilotar un mÃ³dulo de alfabetizaciÃ³n en IA financiera diseÃ±ado especÃ­ficamente como experimento controlado: un grupo recibe el mÃ³dulo, otro no, y se mide satisfacciÃ³n financiera y comportamiento de ahorro a 6 meses. El objetivo del piloto es determinar si la adopciÃ³n de IA en usuarios de ingreso bajo-medio produce mejoras medibles, o si el efecto observado es atribuible al ingreso preexistente.

**Nota de reconciliaciÃ³n:** El ingreso promedio de $1,750 de los usuarios de IA alta podrÃ­a parecer inconsistente con las medianas por industria del Finding 9 ($915â€“$1,066). No hay contradicciÃ³n: las medianas del Finding 9 describen al trabajador tÃ­pico de cada sector. Los usuarios de IA alta no son tÃ­picos â€” el Finding 10 muestra visualmente que son los top earners dentro de cada industria, concentrados por encima de la mediana en todos los sectores. El promedio de $1,750 refleja que dentro de cada caja del boxplot del Finding 9, los puntos de alto uso de IA se ubican sistemÃ¡ticamente en el extremo derecho.

**Mecanismo:** **Alto ingreso precede al uso intensivo de IA, no al revÃ©s**

**Fuente:** Pearson r (IA vs satisfacciÃ³n) = 0.571; r (IA vs ingreso) = 0.634; comparaciÃ³n por industria (`scripts/03_analyse.py`)

**CorrelaciÃ³n encontrada con Hallazgo 1:** Brasil y Chile â€” los paÃ­ses de mayor ingreso mediano â€” tambiÃ©n registran los mayores promedios de uso de IA (7.1 y 6.7 hrs/sem), mientras Argentina y Colombia usan menos IA (4.2 y 4.4 hrs/sem). La brecha de acceso a herramientas digitales refuerza la brecha de ingresos entre paÃ­ses.

ðŸ’¡ *Discrepancia real: el Finding 4 muestra que tarjetahabientes ahorran mÃ¡s con casi el mismo ingreso (engagement financiero), y el Finding 5 muestra que usuarios de IA alta tienen mÃ¡s satisfacciÃ³n y mÃ¡s ingreso â€” pero no hay datos que permitan confirmar si son el mismo subgrupo. Si lo son, existe un perfil unificado de "usuario financieramente activo" que el programa podrÃ­a cultivar directamente. Si no lo son, son dos palancas independientes. â€” Sugerencia: en futuras ediciones del estudio, cruzar tenencia de tarjeta con uso de IA para identificar si el perfil se superpone.*

---

## Hallazgo 6: Carga de Vivienda por PaÃ­s

**Los datos:** Argentina (34.1%) y Chile (32.6%) enfrentan las cargas de vivienda mÃ¡s altas de la regiÃ³n, casi 10 puntos por encima de PerÃº (24.6%) que registra la mÃ¡s baja. Crucialmente, Argentina no es el paÃ­s de menor ingreso mediano ($798) â€” Colombia ($857) y PerÃº ($822) tienen ingresos similares con cargas de vivienda de 25.4% y 24.6% respectivamente. La presiÃ³n de vivienda en Argentina y Chile responde a condiciones del mercado inmobiliario, no al nivel de ingresos.

**Â¿Por quÃ© importa?:** En un paÃ­s donde la vivienda absorbe el 34% del ingreso, el margen disponible para todo lo demÃ¡s â€” transporte, alimentaciÃ³n, educaciÃ³n y ahorro â€” es estructuralmente mÃ¡s estrecho. NingÃºn cambio de comportamiento individual puede compensar plenamente esta restricciÃ³n. Un programa que aplica las mismas metas de ahorro en Argentina que en PerÃº estÃ¡ ignorando una diferencia estructural de casi 10 puntos porcentuales de ingreso disponible.

**RecomendaciÃ³n:** Para Argentina y Chile, complementar el currÃ­culo base con un mÃ³dulo de gestiÃ³n de carga de vivienda: evaluaciÃ³n de contratos de arrendamiento, derechos del inquilino, esquemas de vivienda asistida disponibles localmente, y estrategias de vivienda compartida. En PerÃº y Colombia, donde la carga es menor, diseÃ±ar un mÃ³dulo que reencuadre explÃ­citamente el margen liberado como oportunidad de ahorro â€” "tienes 9 puntos porcentuales mÃ¡s disponibles que alguien en Argentina; aquÃ­ estÃ¡ cÃ³mo usarlos".

**Mecanismo:** **PresiÃ³n estructural de mercado independiente del comportamiento individual**

**Fuente:** carga de vivienda promedio por paÃ­s â€” Argentina 34.1%, PerÃº 24.6% (`scripts/03_analyse.py`)

*No se encontrÃ³ correlaciÃ³n significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 7 â€” ValidaciÃ³n: Edad No Predice el Ingreso

**Los datos:** Pearson r (edad vs ingreso) = -0.029, p = 0.519. No existe relaciÃ³n estadÃ­sticamente significativa entre la edad del respondente y su ingreso mensual. Los ingresos promedio por grupo de edad son prÃ¡cticamente idÃ©nticos: 18â€“22 aÃ±os ($1,039), 23â€“25 ($978), 26â€“28 ($1,066), 29â€“32 ($993) â€” una variaciÃ³n mÃ¡xima de $88 entre grupos, dentro del margen de error esperado para muestras de este tamaÃ±o.

> ðŸ“ *Nota metodolÃ³gica: p = 0.519 significa que, si la edad y el ingreso no tuvieran ninguna relaciÃ³n real entre sÃ­, el 51.9% de las veces observarÃ­amos un patrÃ³n igual o mÃ¡s extremo que el que vemos â€” solo por azar. Eso es mÃ¡s de la mitad de las veces. Cuando el azar puede explicar lo que vemos con tanta facilidad, no podemos concluir que existe una relaciÃ³n real. Esto no significa que la relaciÃ³n sea exactamente cero â€” significa que los datos no tienen suficiente evidencia para afirmar que existe.*

**Â¿Por quÃ© importa?:** Este hallazgo de ausencia es la pieza que hace coherente el Hallazgo 2. Si los jÃ³venes de 18â€“22 ganaran significativamente menos que los de 29â€“32, la brecha de ahorro podrÃ­a explicarse por restricciÃ³n econÃ³mica y el programa tendrÃ­a poco margen de acciÃ³n. El Hallazgo 7 cierra esa salida: los cuatro grupos de edad tienen prÃ¡cticamente el mismo ingreso, lo que convierte la brecha de ahorro en un problema de hÃ¡bito con soluciÃ³n educativa, no de acceso econÃ³mico con soluciÃ³n de polÃ­tica pÃºblica.

**RecomendaciÃ³n:** Este hallazgo no genera un mÃ³dulo propio â€” su funciÃ³n es validar la recomendaciÃ³n del Hallazgo 2. Permite al equipo de programa argumentar con evidencia que el mÃ³dulo de ahorro automatizado para 18â€“22 aÃ±os es la intervenciÃ³n de mayor retorno, porque esta poblaciÃ³n tiene capacidad econÃ³mica comprobada que no estÃ¡ convirtiendo en ahorro.

**Mecanismo:** **La ausencia de relaciÃ³n como evidencia â€” la brecha es conductual, no econÃ³mica**

**Fuente:** Pearson r = -0.029, p = 0.519; ingresos promedio por grupo de edad (`scripts/03_analyse.py`, Finding 7)

*No se encontrÃ³ correlaciÃ³n significativa con hallazgos anteriores adicional a la validaciÃ³n del Hallazgo 2.*
*Sin discrepancias detectadas.*

---

## Hallazgo 8 â€” ValidaciÃ³n: Proporciones de Gasto Estables por Edad

**Los datos:** Las proporciones de gasto por categorÃ­a son prÃ¡cticamente idÃ©nticas entre los cuatro grupos de edad. Vivienda oscila entre 27.5% y 29.1% del ingreso; alimentaciÃ³n entre 23.6% y 24.1%; transporte entre 9.4% y 10.7%; entretenimiento entre 8.5% y 8.9%. Ninguna categorÃ­a muestra una tendencia sistemÃ¡tica creciente o decreciente con la edad.

> ðŸ“ *Nota metodolÃ³gica: "Sin tendencia sistemÃ¡tica" significa que si pusiÃ©ramos los cuatro grupos de edad en orden de menor a mayor, los porcentajes no suben ni bajan de forma consistente â€” suben y bajan de forma aleatoria, como lo harÃ­a el ruido estadÃ­stico normal entre muestras pequeÃ±as. Es diferente a que todos los porcentajes sean exactamente iguales: la variaciÃ³n existe, pero no tiene direcciÃ³n.*

**Â¿Por quÃ© importa?:** Este hallazgo responde una hipÃ³tesis alternativa importante: si los jÃ³venes de 18â€“22 ahorraran menos porque gastan proporcionalmente mÃ¡s en entretenimiento o alimentaciÃ³n, habrÃ­a justificaciÃ³n para un mÃ³dulo de control de gastos discrecionales diferenciado por edad. Los datos refutan esta hipÃ³tesis directamente. La estructura de gasto es casi uniforme entre grupos â€” lo que varÃ­a no es cÃ³mo gastan sino si ahorran el margen que queda despuÃ©s de gastar. Esto refuerza el Hallazgo 3 y consolida la narrativa del Hallazgo 2: el problema es de hÃ¡bito, no de estructura.

**RecomendaciÃ³n:** Al igual que el Hallazgo 7, este hallazgo valida recomendaciones existentes mÃ¡s que generar una nueva. Permite descartar la hipÃ³tesis de que el mÃ³dulo mÃ¡s importante para 18â€“22 aÃ±os es "control de gastos discrecionales". La evidencia apunta a que el mÃ³dulo mÃ¡s efectivo es "ahorro automatizado antes de cualquier gasto", porque la distribuciÃ³n de gastos ya es razonablemente eficiente en todos los grupos de edad.

**Mecanismo:** **La estructura de gastos es universal; el hÃ¡bito de ahorro es lo que varÃ­a con la edad**

**Fuente:** proporciones de gasto por grupo de edad â€” vivienda 27.5%â€“29.1%, entretenimiento 8.5%â€“8.9% (`scripts/03_analyse.py`, Finding 8)

*No se encontrÃ³ correlaciÃ³n significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 9 â€” Suplementario: Ingreso por Industria

**Los datos:** Las medianas sectoriales varÃ­an entre $915 (Marketing) y $1,066 (Recursos Humanos) â€” una brecha de apenas $151. Sin embargo, la dispersiÃ³n interna es dramÃ¡tica: Finanzas muestra ingresos de $300 a $2,874 dentro del mismo sector; TecnologÃ­a de $300 a $2,092; IngenierÃ­a de $300 a $2,524. La industria elegida predice poco el ingreso mediano en etapa temprana de carrera; la posiciÃ³n dentro de esa industria lo predice todo.

> ðŸ“ *Nota metodolÃ³gica: "DispersiÃ³n" mide quÃ© tan separados estÃ¡n los valores entre sÃ­. Una dispersiÃ³n alta significa que dentro de ese grupo hay personas con valores muy distintos. Que Finanzas tenga ingresos de $300 a $2,874 quiere decir que un analista financiero reciÃ©n egresado y un director de finanzas estÃ¡n en el mismo grupo â€” sus ingresos son radicalmente distintos, aunque ambos trabajan en "Finanzas".*

**Â¿Por quÃ© importa?:** Un programa que segmenta a sus participantes Ãºnicamente por industria estarÃ¡ agrupando perfiles financieros radicalmente distintos bajo la misma etiqueta. DiseÃ±ar mÃ³dulos "para profesionales de tecnologÃ­a" sin distinguir su posiciÃ³n en la distribuciÃ³n de ingresos de su sector es ignorar la variable que mÃ¡s impacta su capacidad de ahorro â€” que no es la industria sino dÃ³nde se ubican dentro de ella.

**RecomendaciÃ³n:** En el diagnÃ³stico inicial del programa, ademÃ¡s de industria y paÃ­s, incluir una pregunta de posiciÃ³n relativa ("Â¿tus ingresos son mÃ¡s altos, similares o mÃ¡s bajos que los de tus colegas con la misma experiencia?"). Usar esta autoevaluaciÃ³n como proxy de posiciÃ³n dentro de la distribuciÃ³n sectorial para personalizar las metas de ahorro, en lugar de usar la industria como variable Ãºnica de segmentaciÃ³n.

**Mecanismo:** **La posiciÃ³n dentro de la industria predice el ingreso; la industria en sÃ­, no**

**Fuente:** medianas sectoriales $915â€“$1,066; dispersiÃ³n interna Finanzas $300â€“$2,874 (`scripts/03_analyse.py`, Finding 9)

**CorrelaciÃ³n con Hallazgo 10:** El Hallazgo 10 muestra que los usuarios de IA alta estÃ¡n concentrados en los extremos superiores de la distribuciÃ³n de cada industria. El Hallazgo 9 explica por quÃ© esto importa: son exactamente los mismos extremos con ingresos de $2,000+ dentro de sectores con medianas de $900. Los usuarios de IA alta no son representativos de su industria â€” son los outliers de alto ingreso dentro de ella.

*Sin discrepancias detectadas.*

---

## Hallazgo 10 â€” Suplementario: Usuarios de IA Alta dentro de la DistribuciÃ³n de Ingreso por Industria

**Los datos:** Los 21 usuarios de alto uso de IA (11+ hrs/sem) no estÃ¡n distribuidos aleatoriamente entre industrias â€” se concentran en el extremo superior de la distribuciÃ³n de ingresos de cada sector. Su ingreso promedio supera la mediana de su industria en rangos que van del 53.9% (Salud) al 142.7% (EducaciÃ³n). Pearson r (horas IA vs ingreso) = 0.634, p < 0.0001.

**Â¿Por quÃ© importa?:** El Hallazgo 5 habÃ­a mostrado que usuarios de IA alta tienen mayor satisfacciÃ³n e ingreso ($1,750 promedio). El Hallazgo 10 revela que este diferencial no es porque estÃ©n en industrias de mayor ingreso â€” es porque son los top earners dentro de cualquier industria que elijan. Esto fortalece la interpretaciÃ³n de que el alto ingreso precede al uso intensivo de IA (y a la satisfacciÃ³n que este trae), mÃ¡s que al revÃ©s.

**RecomendaciÃ³n:** No asumir que un mÃ³dulo de IA financiera por sÃ­ solo mejorarÃ¡ los resultados de participantes de ingreso bajo-medio. Antes de escalar ese mÃ³dulo, pilotarlo como experimento controlado (ver Hallazgo 5) para distinguir si el beneficio es del mÃ³dulo o del perfil de ingreso preexistente.

**Nota de reconciliaciÃ³n:** El ingreso promedio de $1,750 de los usuarios de IA alta (Hallazgo 5) podrÃ­a parecer inconsistente con las medianas sectoriales de $915â€“$1,066 del Hallazgo 9. No hay contradicciÃ³n: el Hallazgo 10 muestra que los usuarios de IA alta no son el trabajador tÃ­pico de su sector â€” son los outliers de alto ingreso dentro de cada caja del boxplot, lo que explica cÃ³mo su promedio puede estar muy por encima de la mediana sectorial.

**Mecanismo:** **Alto ingreso precede al uso intensivo de IA dentro de cada industria**

**Fuente:** ingreso promedio de usuarios IA alta vs mediana sectorial â€” 54% a 143% por encima; r = 0.634, p < 0.0001 (`scripts/03_analyse.py`, Finding 10)

*Sin discrepancias detectadas.*

---

## Hallazgo 11: Cuenta de Ahorro vs. Comportamiento Real de Ahorro

**Los datos:** Los respondentes con cuenta de ahorro (n=362) ahorran apenas 3% mÃ¡s que quienes no tienen una ($100.49 vs $97.58/mes) con solo 0.5% mÃ¡s de ingreso ($1,018 vs $1,013/mes). La diferencia en satisfacciÃ³n financiera es igualmente marginal (+3.4%). El coeficiente de Pearson entre tener cuenta de ahorro y el monto ahorrado es r = 0.014 (p = 0.760) â€” estadÃ­sticamente indistinguible de cero.

**Â¿Por quÃ© importa?:** El 72.4% de los respondentes tiene cuenta de ahorro, lo que podrÃ­a sugerir que el acceso al instrumento resuelve el problema. Los datos refutan esto directamente: tener la cuenta no predice ahorrar mÃ¡s. El instrumento sin el hÃ¡bito es inerte. Esto contrasta con el Finding 4 donde la tarjeta de crÃ©dito sÃ­ se asocia con mayor ahorro (+6.7%) â€” la diferencia es que la tarjeta implica un ciclo de uso activo mensual, mientras la cuenta de ahorro puede existir sin ser utilizada.

**RecomendaciÃ³n:** No diseÃ±ar mÃ³dulos orientados a "abrir una cuenta de ahorro" como meta en sÃ­ misma. En cambio, el mÃ³dulo de ahorro debe centrarse en el comportamiento de transferencia automÃ¡tica â€” la cuenta es el contenedor, pero la transferencia programada es el hÃ¡bito. La meta medible del mÃ³dulo debe ser "transferencia configurada y ejecutada el primer mes", no "cuenta abierta".

**Mecanismo:** **El instrumento sin el hÃ¡bito es inerte**

**Fuente:** r (cuenta_ahorro vs ahorro_mensual) = 0.014, p = 0.760 (`scripts/03_analyse.py`)

**CorrelaciÃ³n con Hallazgo 4:** El Finding 4 muestra que tarjetahabientes ahorran 6.7% mÃ¡s â€” contrario al 3% no significativo de los cuentahabientes. Ambos son instrumentos financieros, pero la tarjeta implica uso activo mensual mientras la cuenta puede permanecer pasiva indefinidamente. Esto refuerza el mecanismo del Finding 4: es el involucramiento activo, no la tenencia del instrumento, lo que predice el ahorro.

*Sin discrepancias detectadas.*

---

## Hallazgo 12: Deuda vs. Ahorro y SatisfacciÃ³n Financiera

**Los datos:** Los respondentes con deuda activa (n=234, deuda promedio $3,952) ahorran 5.1% mÃ¡s que quienes no tienen deuda ($101.49 vs $96.61/mes), pero reportan 2.7% menos satisfacciÃ³n financiera (2.46 vs 2.53). La correlaciÃ³n entre tener deuda y el monto ahorrado es r = 0.026 (p = 0.564) â€” no significativa. Los ingresos de ambos grupos son prÃ¡cticamente idÃ©nticos ($1,019 vs $1,015/mes).

**Â¿Por quÃ© importa?:** La imagen popular de la deuda como enemiga del ahorro no estÃ¡ respaldada por estos datos: quienes tienen deuda ahorran marginalmente mÃ¡s, no menos. Lo que la deuda sÃ­ comprime es el bienestar percibido â€” la satisfacciÃ³n financiera cae aunque el comportamiento de ahorro no. Esto sugiere que la deuda opera principalmente como carga psicolÃ³gica, no como restricciÃ³n de flujo de caja en esta muestra.

**RecomendaciÃ³n:** DiseÃ±ar un mÃ³dulo de gestiÃ³n de deuda orientado al bienestar percibido, no solo al pago: tÃ©cnicas de priorizaciÃ³n de deuda (avalancha vs bola de nieve), comunicaciÃ³n de progreso visible, y separaciÃ³n mental entre "deuda bajo control" y "deuda problemÃ¡tica". El objetivo no es solo reducir el saldo â€” es reducir la carga cognitiva que la deuda produce sobre la satisfacciÃ³n financiera.

**Mecanismo:** **La deuda comprime el bienestar, no el ahorro**

**Fuente:** ahorro promedio con/sin deuda: $101.49 vs $96.61; satisfacciÃ³n: 2.46 vs 2.53; r = 0.026, p = 0.564 (`scripts/03_analyse.py`)

*No se encontrÃ³ correlaciÃ³n significativa adicional con hallazgos anteriores.*
*Sin discrepancias detectadas.*

---

## Hallazgo 13: Meta Financiera vs. Tasa de Ahorro Real

**Los datos:** Los respondentes cuya meta es "Ahorrar para viaje" tienen la tasa de ahorro mÃ¡s alta (10.8%, $112/mes), seguidos de "Fondo de emergencia" (11.0%, $107/mes) y "Comprar casa" (10.5%, $108/mes). En el extremo opuesto, "Ahorrar para retiro" registra la tasa mÃ¡s baja de todas (8.0%, $77/mes) y "Estudiar posgrado" la segunda mÃ¡s baja (8.4%, $91/mes). Los ingresos entre grupos son comparables ($941â€“$1,080/mes), por lo que la diferencia no se explica por capacidad econÃ³mica.

**Â¿Por quÃ© importa?:** El hallazgo contradice la intuiciÃ³n de que las metas mÃ¡s serias o a largo plazo generan mayor disciplina. Ocurre exactamente lo contrario: las metas concretas, cercanas y visualizables ("viaje", "casa", "emergencia") producen tasas de ahorro consistentemente mÃ¡s altas que las abstractas y lejanas ("retiro", "posgrado"). Un programa que empuje a jÃ³venes de 18â€“22 aÃ±os a ahorrar para el retiro como primera meta estÃ¡ eligiendo el instrumento de menor efectividad comprobada en esta muestra.

**RecomendaciÃ³n:** Estructurar el mÃ³dulo de metas financieras en dos niveles: primero una meta concreta de horizonte corto (3â€“12 meses) que genere el hÃ¡bito de ahorro y la experiencia de lograrlo, y solo despuÃ©s introducir metas de largo plazo como el retiro. El progreso visible hacia una meta cercana es el mecanismo que sostiene el hÃ¡bito â€” no la importancia abstracta de la meta.

**Mecanismo:** **Metas concretas y cercanas generan mÃ¡s ahorro que metas abstractas y lejanas**

**Fuente:** tasa de ahorro por meta financiera â€” retiro 8.0%, viaje 10.8% (`scripts/03_analyse.py`); grÃ¡fica `charts/11_goal_vs_savings_rate.png`

**CorrelaciÃ³n con Hallazgo 2:** El Finding 2 identificÃ³ que los jÃ³venes de 18â€“22 ahorran menos por falta de hÃ¡bito. El Finding 13 aÃ±ade un mecanismo: si el programa les asigna metas de largo plazo (retiro) como primera intervenciÃ³n, estÃ¡ reforzando el patrÃ³n de bajo ahorro en lugar de romperlo. La secuencia correcta es: meta cercana â†’ hÃ¡bito â†’ meta de largo plazo.

ðŸ’¡ *Discrepancia real: el Finding 13 muestra que "Pagar deudas" tiene una tasa de ahorro media (9.1%) â€” pero el Finding 12 muestra que tener deuda no reduce el ahorro significativamente. Esto podrÃ­a indicar que quienes tienen deuda como meta ya la estÃ¡n gestionando activamente (y por eso ahorran a tasa normal), mientras quienes tienen deuda pero otra meta financiera son los que muestran menor bienestar. â€” Sugerencia: en futuras ediciones del estudio, cruzar tiene_deuda con meta_financiera para identificar si la alineaciÃ³n entre situaciÃ³n financiera real y meta declarada predice mejores resultados.*

---

## Hallazgo 14: Tarjetahabientes â€” Gasto Desglosado por CategorÃ­a

**Los datos:** El gasto adicional de los tarjetahabientes frente a no tarjetahabientes se concentra en dos categorÃ­as: alimentaciÃ³n (+16.1%, $258 vs $222/mes) y entretenimiento (+17.2%, $95 vs $81/mes). Las categorÃ­as estructurales son casi idÃ©nticas entre grupos: vivienda (+1.4%), transporte (+3.9%), salud (+4.8%). La educaciÃ³n muestra una diferencia media (+9.5%) que podrÃ­a reflejar pagos de cursos o plataformas digitales procesados con tarjeta.

**Â¿Por quÃ© importa?:** Este desglose resuelve una ambigÃ¼edad del Finding 4, que solo mostraba totales. El gasto adicional de tarjetahabientes no estÃ¡ distribuido uniformemente â€” estÃ¡ concentrado en las categorÃ­as mÃ¡s discrecionales y mÃ¡s susceptibles de variar mes a mes. Esto es consistente con un perfil de uso de tarjeta para consumo cotidiano (restaurantes, entretenimiento) mÃ¡s que para gastos estructurales. Combinado con el hecho de que tambiÃ©n ahorran mÃ¡s, sugiere que la tarjeta facilita el gasto discrecional sin comprometer el ahorro â€” posiblemente porque el ciclo mensual de la tarjeta crea una revisiÃ³n implÃ­cita del presupuesto.

**RecomendaciÃ³n:** En el mÃ³dulo de crÃ©dito responsable, usar esta distribuciÃ³n como caso de enseÃ±anza: mostrar que el gasto extra de los tarjetahabientes es discrecional (+16â€“17% en alimentos y entretenimiento) pero que no afecta el ahorro (+6.7%). La discusiÃ³n debe centrarse en cÃ³mo distinguir cuÃ¡ndo el gasto discrecional con tarjeta estÃ¡ dentro del presupuesto vs cuÃ¡ndo estÃ¡ financiando consumo que supera el ingreso disponible.

**Mecanismo:** **El exceso de gasto con tarjeta es discrecional, no estructural**

**Fuente:** diferencia por categorÃ­a â€” alimentaciÃ³n +16.1%, entretenimiento +17.2%, vivienda +1.4% (`scripts/03_analyse.py`); grÃ¡fica `charts/12_credit_card_spending_by_category.png`

**CorrelaciÃ³n con Hallazgo 3:** El Finding 3 muestra que entretenimiento representa solo 8.7% del ingreso promedio. El Finding 14 revela que tarjetahabientes gastan 17.2% mÃ¡s en esta categorÃ­a â€” lo que eleva su proporciÃ³n a ~10.2%. Esto confirma que el gasto discrecional adicional de tarjetahabientes es real pero acotado: no redefine la estructura de gasto, solo la amplÃ­a en el margen.

*Sin discrepancias adicionales detectadas.*

---

## GrÃ¡fica 13: Carga de Vivienda vs. Ahorro Promedio por PaÃ­s (`charts/13_vivienda_vs_ahorro.png`)

**Los datos:** El grÃ¡fico muestra los 6 paÃ­ses con carga de vivienda en el eje X y ahorro mensual promedio en el eje Y. El tamaÃ±o de cada punto representa el ingreso mediano. Valores: Brasil (26.9%, $135), Chile (32.6%, $118), MÃ©xico (28.1%, $102), Colombia (25.4%, $82), PerÃº (24.6%, $81), Argentina (34.1%, $77). **Pearson r = 0.037, p = 0.944** â€” correlaciÃ³n prÃ¡cticamente cero.

> ðŸ“ *Nota metodolÃ³gica â€” quÃ© significan r = 0.037 y p = 0.944:*
>
> **r = 0.037** es el coeficiente de correlaciÃ³n de Pearson. Va de -1 a +1. Un valor de +1 significarÃ­a que cuando la carga de vivienda sube, el ahorro sube siempre en la misma proporciÃ³n â€” relaciÃ³n perfecta. Un valor de -1 significarÃ­a lo opuesto: siempre baja. Un valor de 0 significarÃ­a que no hay relaciÃ³n: conocer la carga de vivienda de un paÃ­s no te dice nada sobre su ahorro. r = 0.037 estÃ¡ tan cerca de cero que es prÃ¡cticamente ruido â€” equivale a decir que la carga de vivienda explica apenas el 0.14% de la variaciÃ³n en ahorro entre paÃ­ses (rÂ² = 0.037Â² â‰ˆ 0.001, o sea, el 0.1%).
>
> **p = 0.944** es el p-valor. Responde esta pregunta: "Si no hubiera ninguna relaciÃ³n real entre estas dos variables, Â¿quÃ© tan probable serÃ­a obtener datos que parecieran tan correlacionados como los nuestros, solo por azar?" p = 0.944 significa que si no existiera ninguna relaciÃ³n real, el 94.4% de las veces â€” casi siempre â€” verÃ­amos un patrÃ³n igual o mÃ¡s "correlacionado" que el nuestro, solo por variaciÃ³n aleatoria. En otras palabras: nuestros datos son completamente normales incluso si la relaciÃ³n es cero. Lo contrario de significativo.
>
> **Â¿Por quÃ© no aceptamos valores con p > 0.05 (y mucho menos p > 0.10)?** La convenciÃ³n estadÃ­stica establece que para afirmar que una relaciÃ³n es real y no producto del azar, el p-valor debe ser menor a 0.05 â€” es decir, la probabilidad de ver ese resultado por azar deberÃ­a ser menor al 5%. Algunos campos aceptan hasta p < 0.10 como "resultado marginal o sugestivo" con cautela. Por encima de 0.10 (mÃ¡s de 1 en 10 posibilidades de que sea azar), los resultados son estadÃ­sticamente inconcluyentes: no podemos distinguir una relaciÃ³n real del ruido aleatorio. p = 0.944 estÃ¡ en el extremo opuesto â€” si publicÃ¡ramos este resultado como hallazgo, estarÃ­amos confundiendo ruido con seÃ±al el 94% de las veces.*

**Â¿Por quÃ© importa?:** El resultado parece contradecir el Hallazgo 6, pero tiene una explicaciÃ³n: el ingreso confunde la relaciÃ³n a nivel de paÃ­s. Brasil tiene la menor carga (26.9%) Y el mayor ahorro ($135) porque tiene el mayor ingreso ($1,458). Argentina tiene la mayor carga (34.1%) Y el menor ahorro ($77) porque tiene el menor ingreso ($798). PerÃº tiene la menor carga (24.6%) pero ahorro bajo ($81) porque su ingreso tambiÃ©n es bajo. El ingreso domina la seÃ±al y la carga de vivienda queda enmascarada. Para aislar el efecto real de la vivienda hay que controlar el ingreso â€” exactamente lo que hace el OLS (AA2).

**RecomendaciÃ³n:** No usar esta grÃ¡fica como evidencia aislada de que "mÃ¡s carga â†’ menos ahorro" â€” los datos de paÃ­s no lo confirman (r = 0.037). Usarla en presentaciones como ilustraciÃ³n de por quÃ© ingreso y vivienda deben analizarse conjuntamente, remitiendo al OLS (AA2) como la herramienta que los separa correctamente.

**Mecanismo:** **El ingreso enmascara el efecto de la vivienda cuando se analiza a nivel de paÃ­s**

**Fuente:** r = 0.037, p = 0.944 (`scripts/06_correlations.py`, `charts/13_vivienda_vs_ahorro.png`)

**CorrelaciÃ³n G13 Ã— F1 y F6:** Esta grÃ¡fica integra F1 (ingreso por paÃ­s, visible en tamaÃ±o del punto) y F6 (carga de vivienda). La ausencia de correlaciÃ³n (r = 0.037) es en sÃ­ misma el hallazgo: el ingreso confunde la relaciÃ³n vivienda-ahorro a nivel agregado.

ðŸ’¡ *Discrepancia real: El Hallazgo 6 implica que mayor carga de vivienda reduce el margen de ahorro, pero la GrÃ¡fica 13 muestra r = 0.037 â€” Chile (carga 32.6%) ahorra $118 mientras PerÃº (carga 24.6%) ahorra solo $81. El mecanismo es que el ingreso domina sobre la vivienda al comparar paÃ­ses. Sugerencia: presentar siempre G13 junto al OLS (AA2) que controla por ingreso y aÃ­sla el efecto real de la vivienda.*

---

## GrÃ¡fica 14: Uso de IA vs. SatisfacciÃ³n Financiera por PaÃ­s (`charts/14_ia_vs_satisfaccion.png`)

**Los datos:** Valores por paÃ­s: Brasil (7.1 hrs, satisfacciÃ³n 2.83), Chile (6.7 hrs, 2.71), MÃ©xico (5.5 hrs, 2.50), PerÃº (4.7 hrs, 2.32), Colombia (4.4 hrs, 2.33), Argentina (4.2 hrs, 2.20). **Pearson r = 0.992, p = 0.000** â€” correlaciÃ³n casi perfecta y estadÃ­sticamente significativa incluso con n=6, superando el umbral r > 0.81 requerido. El patrÃ³n individual (F5: r = 0.571) y el patrÃ³n de paÃ­s (r = 0.992) van en la misma direcciÃ³n.

> ðŸ“ *Nota metodolÃ³gica â€” quÃ© significa r = 0.992 y por quÃ© p = 0.000 aquÃ­ sÃ­ es vÃ¡lido:*
>
> **r = 0.992** significa correlaciÃ³n casi perfecta. Para tener una referencia: r = 0.5 es una relaciÃ³n moderada; r = 0.7 es fuerte; r = 0.9 es muy fuerte; r = 0.992 es prÃ¡cticamente una lÃ­nea recta. Si graficÃ¡ramos uso de IA vs. satisfacciÃ³n para los 6 paÃ­ses, los puntos caerÃ­an casi exactamente sobre una lÃ­nea. El 98.4% de la variaciÃ³n en satisfacciÃ³n entre paÃ­ses queda explicada por el uso de IA (rÂ² = 0.992Â² â‰ˆ 0.984).
>
> **p = 0.000** aquÃ­ es vÃ¡lido, a diferencia de la GrÃ¡fica 13. Con n=6 paÃ­ses, normalmente se necesita r > 0.81 para alcanzar p < 0.05 â€” y r = 0.992 lo supera por amplio margen. La razÃ³n por la que esta correlaciÃ³n "pasa el filtro" con solo 6 puntos es precisamente porque es tan extrema (0.992) que serÃ­a casi imposible obtenerla por azar si no hubiera ninguna relaciÃ³n real.
>
> **La advertencia importante:** p = 0.000 confirma que la correlaciÃ³n no es azar, pero no confirma que el uso de IA *cause* la satisfacciÃ³n. Puede ser que un tercer factor â€” el ingreso â€” estÃ© causando ambas cosas simultÃ¡neamente: los paÃ­ses mÃ¡s ricos (Brasil, Chile) tienen mÃ¡s dinero para comprar herramientas digitales Y mÃ¡s razones para estar satisfechos financieramente. La correlaciÃ³n es real; la causalidad no estÃ¡ demostrada.*

**Â¿Por quÃ© importa?:** Esta es la Ãºnica correlaciÃ³n del proyecto que es significativa tanto a nivel individual (F5: r = 0.571) como a nivel de paÃ­s (r = 0.992). La consistencia entre dos niveles de anÃ¡lisis distintos fortalece la asociaciÃ³n â€” pero el ingreso sigue siendo el confundidor principal. Los paÃ­ses mÃ¡s ricos (Brasil, Chile) usan mÃ¡s IA y tienen mayor satisfacciÃ³n; los mÃ¡s pobres (Argentina, Colombia) usan menos y tienen menor satisfacciÃ³n. La correlaciÃ³n puede ser real, puede ser espuria, o puede ser ambas cosas simultÃ¡neamente a distintas escalas.

**RecomendaciÃ³n:** Presentar G14 junto a F5 como evidencia de consistencia multi-nivel: "el patrÃ³n IA-satisfacciÃ³n existe tanto entre individuos como entre paÃ­ses". Siempre acompaÃ±arla del OLS (AA2) que muestra que el efecto de la IA sobre el ahorro desaparece al controlar el ingreso â€” la asociaciÃ³n es consistente pero la causalidad no estÃ¡ demostrada.

**Mecanismo:** **Uso de IA y satisfacciÃ³n co-varÃ­an a nivel de paÃ­s, mediados por el ingreso**

**Fuente:** r = 0.992, p = 0.000 (`scripts/06_correlations.py`, `charts/14_ia_vs_satisfaccion.png`)

**CorrelaciÃ³n G14 Ã— F5 y F1:** El patrÃ³n paÃ­s-nivel (G14) es consistente con el patrÃ³n individual (F5: r = 0.571). F1 aÃ±ade el contexto: los paÃ­ses de mayor ingreso son los de mayor uso de IA y mayor satisfacciÃ³n, sugiriendo que el ingreso es la variable mediadora en ambos niveles de anÃ¡lisis.

ðŸ’¡ *Discrepancia real: La GrÃ¡fica 14 muestra r = 0.992 a nivel de paÃ­s, pero el OLS (AA2) muestra que el efecto de la IA sobre el ahorro no es significativo cuando se controla el ingreso (p = 0.657). Los dos anÃ¡lisis no se contradicen â€” uno mide satisfacciÃ³n y el otro ahorro, y operan a distintos niveles â€” pero un lector no tÃ©cnico podrÃ­a leer "IA predice satisfacciÃ³n perfectamente" y "IA no predice ahorro" como contradicciÃ³n. Sugerencia: presentar siempre G14 y OLS juntos con nota explÃ­cita de que miden variables y niveles distintos.*

---

## AnÃ¡lisis Avanzado 1: Perfil de Ahorradores Negativos (`charts/15_negative_savers_profile.png`)

**Los datos:** 74 de los 500 participantes (14.8%) reportaron ahorro mensual negativo en el perÃ­odo encuestado â€” es decir, gastaron mÃ¡s de lo que ingresaron ese mes. La concentraciÃ³n por edad es clara: el 24.7% del grupo de 18â€“22 aÃ±os tiene ahorro negativo, frente a apenas el 2.3% del grupo de 29â€“32. La distribuciÃ³n por paÃ­s muestra que PerÃº (20.0%), Colombia (18.8%) y Brasil (15.4%) tienen las proporciones mÃ¡s altas. El perfil de este subgrupo muestra ingresos ligeramente menores que los ahorradores positivos ($918 vs $1,034), mayor uso de tarjeta de crÃ©dito y niveles similares de deuda activa.

> ðŸ“ *Nota metodolÃ³gica: "Ahorro negativo" no significa que alguien perdiÃ³ dinero de sus ahorros acumulados. Significa que en el mes encuestado gastÃ³ mÃ¡s de lo que ingresÃ³ â€” lo que puede ocurrir por usar crÃ©dito, tomar dinero de ahorros previos, o recibir apoyo de terceros. Es como cuando uno "va en rojo" ese mes. No dice nada sobre su situaciÃ³n financiera histÃ³rica, solo sobre ese perÃ­odo.*

**Â¿Por quÃ© importa?:** Este subgrupo representa casi 1 de cada 6 participantes y es el de mayor urgencia del programa â€” pero es tambiÃ©n el mÃ¡s difÃ­cil de retener, porque quienes estÃ¡n en crisis financiera inmediata tienen menor capacidad de atenciÃ³n para mÃ³dulos educativos. El hecho de que el 24.7% de los jÃ³venes de 18â€“22 estÃ© en esta situaciÃ³n, frente al 2.3% de los de 29â€“32, refuerza que el problema no es estructural sino de etapa de vida: los participantes de mÃ¡s edad han salido de esta zona por acumulaciÃ³n de experiencia y hÃ¡bito, no por mayor ingreso (Hallazgo 7).

**RecomendaciÃ³n:** Crear un mÃ³dulo de "estabilizaciÃ³n de emergencia" especÃ­fico para el subgrupo de ahorro negativo, separado del currÃ­culo base. Este mÃ³dulo debe tener horizonte de 30â€“60 dÃ­as y metas mÃ­nimas alcanzables (reducir el dÃ©ficit mensual, no alcanzar ahorro positivo de inmediato). Identificar a estos participantes en el diagnÃ³stico inicial y derivarlos a esta ruta antes de cualquier otro mÃ³dulo.

**Mecanismo:** **DÃ©ficit mensual como estado transitorio de etapa de vida, no como condiciÃ³n estructural permanente**

**Fuente:** 74/500 participantes con ahorro negativo; concentraciÃ³n en 18â€“22 aÃ±os: 24.7% vs 29â€“32: 2.3% (`scripts/07_advanced.py`, SecciÃ³n 1)

**CorrelaciÃ³n con Hallazgos 2 y 6:** El Hallazgo 2 muestra que los jÃ³venes de 18â€“22 ahorran menos en general. El AnÃ¡lisis Avanzado 1 revela que dentro de ese grupo, una cuarta parte estÃ¡ en dÃ©ficit â€” no solo en ahorro bajo. El Hallazgo 6 (carga de vivienda) puede ser un factor agravante para los ahorradores negativos, cuya carga de vivienda (27.4%) es comparable a la del resto de la muestra pero combinada con menor ingreso produce dÃ©ficit mÃ¡s fÃ¡cilmente.

*Sin discrepancias detectadas.*

---

## AnÃ¡lisis Avanzado 2: RegresiÃ³n OLS â€” Â¿QuÃ© Predice el Ahorro? (`charts/16_ols_coefficients.png`)

**Los datos:** La regresiÃ³n OLS con 6 predictores explica el 26.8% de la varianza en el ahorro mensual (RÂ² = 0.268). El error promedio del modelo es $82.31 USD (RMSE). Solo dos variables son estadÃ­sticamente significativas: edad (+$38.16 USD por cada desviaciÃ³n estÃ¡ndar de edad, equivalente a ~4.2 aÃ±os; p < 0.001) e ingreso mensual (+$31.45 USD por desviaciÃ³n estÃ¡ndar; p < 0.001). Las cuatro variables restantes â€” uso de IA, tarjeta de crÃ©dito, cuenta de ahorro y deuda activa â€” no tienen efecto significativo independiente (todos p > 0.60) cuando se controlan la edad y el ingreso.

> ðŸ“ *Nota metodolÃ³gica: Una regresiÃ³n OLS (MÃ­nimos Cuadrados Ordinarios) hace algo que los anÃ¡lisis individuales de los Hallazgos 1â€“14 no podÃ­an hacer: ver el efecto de cada variable mientras mantiene las demÃ¡s constantes. Es como comparar dos personas idÃ©nticas en todo â€” misma edad, mismo ingreso, mismo paÃ­s â€” excepto en que una tiene tarjeta de crÃ©dito y la otra no. La regresiÃ³n pregunta: en esa comparaciÃ³n, Â¿la tarjeta predice mÃ¡s ahorro? Si la respuesta es "no" (p alto), el efecto que habÃ­amos visto en el Hallazgo 4 probablemente ocurrÃ­a porque los tarjetahabientes tambiÃ©n tenÃ­an mayores ingresos o edades â€” no por la tarjeta en sÃ­. "DesviaciÃ³n estÃ¡ndar" es una forma de medir cuÃ¡nto varÃ­a algo. Decir que la edad sube $38 por SD significa que pasar de ser "joven promedio" a "algo mayor que el promedio" predice $38 mÃ¡s de ahorro mensual.*

**Â¿Por quÃ© importa?:** Este anÃ¡lisis es el test mÃ¡s riguroso del proyecto. Cuando se controla por todo lo demÃ¡s, el resultado es contundente: la edad y el ingreso son los dos Ãºnicos predictores robustos del ahorro. Los instrumentos financieros â€” tarjeta, cuenta de ahorro, uso de IA, deuda â€” pierden su poder predictivo cuando se les compara dentro del mismo perfil de edad e ingreso. Esto confirma el mecanismo central del Hallazgo 11 desde un Ã¡ngulo completamente diferente: el instrumento sin el hÃ¡bito es inerte.

**RecomendaciÃ³n:** Usar estos resultados para priorizar el currÃ­culo: invertir primero en el hÃ¡bito de ahorro (edad como proxy de acumulaciÃ³n de experiencia) y en estrategias de crecimiento de ingreso dentro de la industria (Hallazgo 9). Los mÃ³dulos de instrumentos financieros (tarjeta, IA, cuenta) tienen valor educativo pero no deben presentarse como predictores independientes de mayor ahorro â€” los datos muestran que su efecto, cuando se aÃ­sla, no es estadÃ­sticamente distinguible de cero.

**Mecanismo:** **Edad e ingreso como Ãºnicos predictores robustos del ahorro; los instrumentos son neutros en igualdad de condiciones**

**Fuente:** RÂ² = 0.268, RMSE = $82.31, N = 500; coeficientes edad +$38.16 p<0.001, ingreso +$31.45 p<0.001 (`scripts/07_advanced.py`, SecciÃ³n 2)

**CorrelaciÃ³n con Hallazgos 4, 5 y 11:** El OLS reconcilia tres hallazgos aparentemente contradictorios. El Hallazgo 4 mostraba que tarjetahabientes ahorran mÃ¡s (+6.7%) y el Hallazgo 5 que usuarios de IA alta tambiÃ©n. El Hallazgo 11 ya sugerÃ­a que la cuenta de ahorro no predice nada. El OLS unifica los tres: ningÃºn instrumento tiene efecto independiente. Las diferencias de los Hallazgos 4 y 5 ocurrÃ­an porque esos grupos tenÃ­an perfiles de edad e ingreso ligeramente distintos.

*Sin discrepancias detectadas.*

---

## AnÃ¡lisis Avanzado 3: SegmentaciÃ³n â€” Tres Perfiles de Usuario (`charts/17_user_clusters.png`)

**Los datos:** El algoritmo de clustering identificÃ³ tres grupos naturales en los datos, diferenciados principalmente por ingreso, presencia de deuda y uso de IA. "En Riesgo" (n=170): ingreso $809, ahorro $75, satisfacciÃ³n 2.20, sin deuda activa. "En Camino" (n=178): ingreso $884, ahorro $85, satisfacciÃ³n 2.26, 100% con deuda activa. "Avanzado" (n=152): ingreso $1,405, ahorro $142, satisfacciÃ³n 3.05, 37% con deuda, 8 hrs/sem de IA frente a 3.9â€“4.6 de los otros grupos.

> ðŸ“ *Nota metodolÃ³gica: El clustering (o segmentaciÃ³n) es un algoritmo que agrupa a las personas en categorÃ­as basÃ¡ndose en su similitud â€” sin que el analista defina las categorÃ­as de antemano. Es como dejar que los datos mismos encuentren sus propios grupos naturales. El grÃ¡fico radar (o de araÃ±a) que acompaÃ±a este anÃ¡lisis muestra cada grupo como un polÃ­gono: los ejes son las variables financieras, y cuanto mÃ¡s grande es el polÃ­gono en un eje, mÃ¡s alto es ese grupo en esa dimensiÃ³n. Si un polÃ­gono es mucho mÃ¡s grande que otro en "ingreso", ese grupo tiene mÃ¡s ingresos.*

**Â¿Por quÃ© importa?:** Los tres perfiles son cualitativamente distintos y requieren intervenciones distintas. "En Riesgo" no tiene deuda â€” su restricciÃ³n es el ingreso bajo combinado con ausencia de hÃ¡bito. "En Camino" tiene deuda al 100% y satisfacciÃ³n apenas superior â€” responde al mÃ³dulo de gestiÃ³n de deuda y concreciÃ³n de metas. "Avanzado" muestra el perfil objetivo: mÃ¡s ingreso, mÃ¡s ahorro, mÃ¡s uso de IA, mayor satisfacciÃ³n. La distancia entre "En Riesgo" y "Avanzado" es la brecha que el programa debe cerrar, y la segmentaciÃ³n permite diseÃ±ar la ruta de cada punto de partida.

**RecomendaciÃ³n:** Incorporar el diagnÃ³stico de perfil al inicio del programa. Un cuestionario de 5 preguntas (ingreso, ahorro actual, deuda activa, uso de IA, satisfacciÃ³n autorreportada) permite asignar a cada participante a uno de los tres perfiles y derivarlos al mÃ³dulo de entrada correspondiente. No usar un currÃ­culo Ãºnico: los tres perfiles requieren Ã©nfasis distintos (ingreso y hÃ¡bito para "En Riesgo", deuda y metas para "En Camino", consolidaciÃ³n y herramientas para "Avanzado").

**Mecanismo:** **Tres rutas de entrada al programa segÃºn el perfil financiero inicial**

**Fuente:** k-means k=3; perfiles: En Riesgo n=170 $809, En Camino n=178 $884, Avanzado n=152 $1,405 (`scripts/07_advanced.py`, SecciÃ³n 3)

**CorrelaciÃ³n con Hallazgos 2, 12 y 13:** El perfil "En Camino" (100% deuda) corresponde al subgrupo del Hallazgo 12 que tiene menor satisfacciÃ³n pese a mayor ingreso. El perfil "En Riesgo" corresponde al extremo joven del Hallazgo 2. La meta de "Invertir en bolsa" del grupo "Avanzado" confirma el Hallazgo 13: quienes ya tienen hÃ¡bito de ahorro eligen metas de mayor complejidad.

*Sin discrepancias detectadas.*

---

## AnÃ¡lisis Avanzado 4: Robustez EstadÃ­stica â€” CorrecciÃ³n FDR Benjamini-Hochberg (`charts/18_fdr_bh_correction.png`)

**Los datos:** 11 tests estadÃ­sticos formales del proyecto (5 correlaciones de Pearson + 6 coeficientes de la regresiÃ³n OLS) fueron evaluados con correcciÃ³n Benjamini-Hochberg al nivel FDR = 0.05. Resultados: 4 tests sobreviven la correcciÃ³n â€” OLS: Edad (p < 0.001), OLS: Ingreso (p < 0.001), F5: IA vs satisfacciÃ³n (p = 0.0001), F10: IA vs ingreso (p = 0.0001). Los 7 tests restantes no son significativos y la correcciÃ³n no cambia su estatus. No hay ningÃºn test en la "zona gris" de p = 0.01â€“0.10.

> ðŸ“ *Nota metodolÃ³gica: Cuando hacemos muchas pruebas estadÃ­sticas sobre los mismos datos, aumenta la probabilidad de que alguna salga "significativa" solo por azar â€” como lanzar una moneda 11 veces: es probable que salga cara varias veces seguidas aunque la moneda sea justa. La correcciÃ³n de Benjamini-Hochberg (BH) ajusta los umbrales de significancia para tener en cuenta este problema. Un hallazgo que "sobrevive" la correcciÃ³n BH es mÃ¡s confiable que uno que solo pasÃ³ el umbral estÃ¡ndar. La "zona gris" son los tests con p entre 0.01 y 0.10 â€” suficientemente bajos para parecer interesantes, pero suficientemente altos para poder ser falsos positivos. Si hay tests en esa zona, la correcciÃ³n BH puede cambiar su conclusiÃ³n. En este proyecto, no hay ninguno.*

**Â¿Por quÃ© importa?:** Este anÃ¡lisis es la garantÃ­a de calidad estadÃ­stica del proyecto. Confirma que los dos hallazgos significativos principales (IA vs satisfacciÃ³n, IA vs ingreso) no son artefactos de haber corrido muchas pruebas â€” sobreviven el test mÃ¡s exigente disponible. Los hallazgos no significativos (F7, F11, F12) estaban tan lejos del umbral que la correcciÃ³n no cambia nada. La zona gris estÃ¡ vacÃ­a, lo que significa que no hay resultados en riesgo de ser malinterpretados.

**RecomendaciÃ³n:** Incluir la tabla de correcciÃ³n BH en el apÃ©ndice metodolÃ³gico del informe ejecutivo cuando se presente al consejo directivo. Los hallazgos de este proyecto pueden presentarse con confianza estadÃ­stica completa: los significativos son robustos y los no significativos estÃ¡n claramente por encima del umbral.

**Mecanismo:** **ValidaciÃ³n cruzada estadÃ­stica: los hallazgos significativos sobreviven el test mÃ¡s exigente**

**Fuente:** 11 tests evaluados; 4/11 significativos despuÃ©s de correcciÃ³n BH (`scripts/07_advanced.py`, SecciÃ³n 4)

**CorrelaciÃ³n con todos los hallazgos anteriores:** Este anÃ¡lisis es el cierre metodolÃ³gico del proyecto. Valida que F5 y F10 (los dos hallazgos de IA) son robustos, y confirma que F7, F11 y F12 son genuinamente nulos â€” no son hallazgos dÃ©biles que una correcciÃ³n podrÃ­a rescatar, sino ausencias de relaciÃ³n bien establecidas.

*Sin discrepancias detectadas.*

---

## ConclusiÃ³n General

**1. La brecha de ahorro es de hÃ¡bito, el instrumento es neutro sin Ã©l, y la meta lo activa o lo suprime**

Los Hallazgos 2, 7 y 8 convergen en una sola conclusiÃ³n, confirmada visualmente en `charts/19_savings_rate_vs_income_by_age.png`: los jÃ³venes de 18â€“22 no ahorran menos porque ganen menos (r = -0.029, p = 0.519, F7) ni porque gasten mÃ¡s proporcionalmente (F8) â€” la tasa de ahorro sube de 6% a 16% mientras el ingreso se mantiene plano. El AnÃ¡lisis Avanzado 2 (OLS) aÃ±ade el nivel mÃ¡s riguroso de evidencia: cuando se controla por edad e ingreso, ningÃºn instrumento financiero â€” tarjeta, cuenta de ahorro, IA, deuda â€” tiene efecto independiente sobre el ahorro (todos p > 0.60). El instrumento sin el hÃ¡bito es inerte (F11, validado por dos mÃ©todos independientes). Y el Hallazgo 13 cierra el argumento con el dato mÃ¡s contraintuitivo del proyecto: los que ahorran para el retiro tienen la tasa mÃ¡s baja (8.0%), mientras los que ahorran para un viaje tienen la mÃ¡s alta (10.8%) â€” la concreciÃ³n de la meta activa el hÃ¡bito, su abstracciÃ³n lo suprime.

**2. El involucramiento activo predice resultados, pero el ingreso es el confundidor en todos los niveles**

Los Hallazgos 4, 5, 10, 14 y la GrÃ¡fica 14 revelan que el involucramiento activo produce mejores resultados â€” pero el ingreso subyace en todos los casos. La GrÃ¡fica 14 muestra r = 0.992 entre uso de IA y satisfacciÃ³n a nivel de paÃ­s (estadÃ­sticamente significativo con n=6), consistente con el F5 individual (r = 0.571) â€” la misma direcciÃ³n en dos niveles de anÃ¡lisis distintos fortalece la asociaciÃ³n. Sin embargo, el F10 muestra que los usuarios de IA alta son top earners dentro de su industria, y el OLS (AA2) confirma que el efecto de la IA desaparece al controlar el ingreso (p = 0.657). La GrÃ¡fica 13 aÃ±ade el contrapunto: la correlaciÃ³n vivienda-ahorro a nivel de paÃ­s es r = 0.037 â€” tambiÃ©n porque el ingreso enmascara la seÃ±al. El ingreso es el confundidor estructural del proyecto en ambas correlaciones cruzadas. El involucramiento activo importa, pero distinguir cuÃ¡nto es del instrumento y cuÃ¡nto del perfil econÃ³mico del participante requiere el experimento controlado del F5.

**3. Las brechas entre paÃ­ses son estructurales y no pueden resolverse solo con mÃ³dulos conductuales**

Los Hallazgos 1, 6 y la GrÃ¡fica 13 muestran que Argentina y Chile tienen cargas de vivienda de 32â€“34% frente al 24â€“25% de PerÃº y Colombia. El AnÃ¡lisis Avanzado 1 aÃ±ade que el 14.8% de los participantes estÃ¡ en dÃ©ficit mensual, con concentraciÃ³n en paÃ­ses de ingreso medio-bajo. El OLS confirma que el ingreso es el segundo predictor mÃ¡s fuerte del ahorro (+$31.45/SD). Esta combinaciÃ³n â€” alta presiÃ³n estructural de vivienda + menor ingreso â€” crea un techo de ahorro que ningÃºn cambio conductual puede superar completamente. El Hallazgo 9 complica aÃºn mÃ¡s el cuadro: dentro de cada paÃ­s e industria, la posiciÃ³n en la distribuciÃ³n de ingresos predice mÃ¡s que la industria en sÃ­. Un currÃ­culo uniforme no puede atender estas realidades divergentes: se requiere calibraciÃ³n por paÃ­s, por perfil de usuario (AnÃ¡lisis Avanzado 3) y por posiciÃ³n en la distribuciÃ³n de ingresos.

**4. La segmentaciÃ³n en tres perfiles transforma el programa de un currÃ­culo Ãºnico a tres rutas de entrada**

El AnÃ¡lisis Avanzado 3 produce la implicaciÃ³n mÃ¡s accionable del proyecto: los 500 participantes se agrupan naturalmente en tres perfiles con necesidades radicalmente distintas â€” "En Riesgo" (n=170, sin deuda, ingreso bajo, sin hÃ¡bito), "En Camino" (n=178, 100% con deuda, ingreso medio, hÃ¡bito parcial), "Avanzado" (n=152, mayor ingreso, mayor uso de IA, mayor satisfacciÃ³n). La distancia entre "En Riesgo" y "Avanzado" es exactamente la brecha que el programa debe cerrar. El AnÃ¡lisis Avanzado 4 (FDR) garantiza que los 4 hallazgos estadÃ­sticamente significativos del proyecto (edad, ingreso, IA-satisfacciÃ³n, IA-ingreso) son robustos y pueden presentarse con confianza al consejo directivo. Las discrepancias abiertas (perfil unificado de usuario activo, relaciÃ³n deuda-meta-ahorro) son preguntas de investigaciÃ³n para la siguiente ediciÃ³n del estudio, no debilidades del anÃ¡lisis actual.

**RecomendaciÃ³n prioritaria**

El mayor impacto del programa se lograrÃ¡ en tres pasos secuenciados. Primero, implementar diagnÃ³stico de perfil al inicio (5 preguntas) para asignar a cada participante a una de las tres rutas del AnÃ¡lisis Avanzado 3. Segundo, para el perfil "En Riesgo" (y especialmente para jÃ³venes de 18â€“22 aÃ±os en Argentina y Chile), arrancar con el mÃ³dulo de estabilizaciÃ³n de emergencia (AnÃ¡lisis Avanzado 1) antes del currÃ­culo base â€” no tiene sentido enseÃ±ar ahorro programado a alguien que termina cada mes en dÃ©ficit. Tercero, en todos los perfiles, estructurar las metas financieras en horizonte corto primero (Hallazgo 13), con transferencia automÃ¡tica configurada desde el primer sueldo (Hallazgo 2), y retroalimentaciÃ³n mensual visible del progreso. Este trÃ­o â€” diagnÃ³stico â†’ estabilizaciÃ³n â†’ hÃ¡bito con meta concreta â€” ataca simultÃ¡neamente la brecha conductual (H2, H7, H8, H11), la crisis de subgrupo vulnerable (AA1) y el mecanismo de activaciÃ³n del ahorro (H13), con evidencia estadÃ­stica robusta respaldada por correcciÃ³n FDR (AA4) en cada paso.
