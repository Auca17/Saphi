# Saphi — Documento de Requisitos de Producto (PRD)

> Estado: Borrador v0.3 · Fecha: 2026-11-18 · Responsable: Auca17
> Idiomas: [English](PRD.md) · Español (este archivo)
> Prototipo: [artifact en vivo](https://claude.ai/artifact/Q6LCHyEBq3khP7uZvdvwQU) · código `prototype/saphi-prototype.html` · Decisiones: [`docs/adr/`](adr/README.md) · Validación: [`docs/validation/interview-guide.md`](validation/interview-guide.md)

**Decisiones clave (ronda de preguntas, 2026-11-18):** usuario principal = principiantes en jardinería; primer mercado = **Mendoza, Argentina**; interfaz en **español rioplatense**; gratis para los usuarios; ingresos futuros con un mapa de viveros pago (ADR 0002); validar en Mendoza antes de construir el backend; 8 a 16 horas por semana mientras la validación se sostenga.

---

## 1. Resumen

Saphi es una **aplicación web mobile-first (PWA)** para planificar y cuidar **jardines ornamentales** y **huertas caseras**. El usuario ingresa el tamaño real de un espacio, obtiene una grilla a escala (el **sandbox**) y ubica plantas con su tamaño adulto. Saphi detecta plantas amontonadas, sombra, pH de suelo incompatible y plantas invasoras; sugiere soluciones, como pasar una planta a una maceta, y ayuda a mantener el espacio con recordatorios, precauciones según el clima y, más adelante, sensores.

**En una frase:** "Mirá tu jardín antes de plantarlo, y mantenelo vivo después."

## 2. Problema

Quienes diseñan o empiezan un jardín tienen dificultades para:

1. **Imaginar la distribución:** cuántas plantas entran, cuánto crecen y dónde van.
2. **Saber qué plantas se llevan bien.** Las plantas no son "enemigas". Algunas se pisan al crecer, otras necesitan otro pH de suelo y otras son invasoras y avanzan sobre sus vecinas.
3. **Evitar la sombra:** las plantas altas le quitan sol a las bajas, y el ángulo del sol cambia con la estación.
4. **Mantener el cuidado:** regar, abonar, cosechar a tiempo y reaccionar ante el clima.

Las herramientas existentes cubren una de estas cosas (planificadores, apps de identificación, controladores de riego), pero no el ciclo completo: **planificar → plantar → cuidar → cosechar**, con una experiencia móvil amigable.

## 3. Usuarios objetivo

| Perfil | Descripción | Necesidad principal |
|---|---|---|
| **Principiante con poco tiempo** (principal) | Vive en Mendoza y empieza con un patio, balcón o terraza. Sabe poco de plantas. | "Decime qué entra, dónde, y cómo protegerlo del granizo, el Zonda y la helada." |
| **Huertero casero** | Cultiva verduras y aromáticas para su casa. | Interacciones entre plantas, momentos de siembra y cosecha. |
| **Paisajista** (segmento futuro) | Diseña jardines para clientes. Necesita software profesional; se atenderá más adelante con un plan Pro (compartir el plan con el cliente, varios proyectos). | Fuera del alcance del MVP. |

**Primer mercado:** Mendoza, Argentina (clima árido, jardines con riego, suelo mayormente alcalino, granizo, viento Zonda, heladas tardías). Después el resto de Argentina y luego otros países.

Fuera de alcance: producción comercial y agrónomos profesionales (ya conocen este tema).

## 4. Objetivos y no-objetivos

### Objetivos
- O1. Un usuario nuevo crea un espacio a escala y ubica plantas en **menos de 5 minutos**, guiado por el tutorial.
- O2. El sandbox marca **amontonamiento, sombra, pH de suelo e invasión** en tiempo real, con una solución cuando existe.
- O3. Los usuarios vuelven cada semana gracias a **recordatorios, precauciones climáticas y gamificación**.
- O4. Los usuarios pagos se quedan porque los buenos hábitos bajan su factura (ver [ADR 0001](adr/0001-plus-achievement-discounts.md)).
- O5. La arquitectura queda preparada para **IA** (asesor, renders, análisis de fotos) y **sensores** sin reescribir.

### No-objetivos
- Sin red social ni feed (alto costo de datos, poco valor).
- Sin app nativa iOS/Android en la v1 (solo PWA).
- Sin agronomía profesional (análisis de laboratorio, modelos de rendimiento comercial).
- Sin venta de hardware en el MVP.

## 5. Principios de producto

1. **Mobile-first, pensado para el pulgar.** Toda acción principal se puede hacer con una mano en una pantalla de ~375 px.
2. **Unidades reales.** La grilla está en centímetros reales. El tamaño de cada planta sale de su tamaño adulto.
3. **Valores por defecto razonables, control total.** Cada planta tiene tamaños por defecto y el usuario puede cambiarlos.
4. **Recomendaciones honestas.** Cada aviso indica qué tan seguro es: *medido*, *documentado*, *tradicional* o *estimado*. La IA nunca inventa datos.
5. **Interfaz tranquila.** Glassmorphism, minimalista, mayormente blanca con verde oscuro y marrón; movimiento suave; sin patrones engañosos en la gamificación; sin explotación de datos.

## 6. Arquitectura de información

Barra de navegación inferior con 4 pestañas, siempre visible:

| Pestaña | Propósito |
|---|---|
| **Inicio** | Tareas del día, racha de cuidado, tus espacios, qué sembrar este mes, clima de 5 días con precauciones. |
| **Jardín** | Espacios ornamentales (sandbox). |
| **Cosecha** | Espacios comestibles (sandbox + línea de tiempo de cosecha). |
| **Perfil** | Nivel, Saphi Plus, logros por niveles, colección de plantas, ajustes (tema, ubicación, hemisferio, tutorial). |

Jardín y Cosecha comparten el **mismo motor de sandbox**. Cambian el catálogo, el objetivo (floración o rendimiento) y la línea de tiempo de Cosecha.

### Diseño de pantalla (Jardín / Cosecha)

```
┌──────────────────────────────────┐
│ Jardín  [Frente de casa ▾]       │  título + selector de espacio
│ 4,0 × 6,0 m · 24 m² · grilla 10 cm │  medidas reales
├──────────────────────────────┬───┤
│                              │ + │  agregar planta
│      SANDBOX (a escala)      │ ☀ │  sol y sombras
│                              │ 👁 │  mostrar problemas
│                              │ ↶ │  deshacer
├──────────────────────────────┴───┤
│ ◯ En maceta  ! Requiere atención  ⋯ Buena pareja  ○ Seleccionada │  referencias
│ Tierra libre 82% · Agua – – – · Problemas 3                      │  franja de datos
│ 🔔 Próximo recordatorio                                           │
├──────────────────────────────────┤
│  Inicio  Jardín  Cosecha  Perfil │  navegación inferior (vidrio)
└──────────────────────────────────┘
```

## 7. Requisitos funcionales

Prioridad: **P0** = MVP · **P1** = inmediatamente después del MVP · **P2** = fase de IA · **P3** = fase de hardware.

### 7.1 Primer uso

| ID | Requisito | Prioridad |
|---|---|---|
| ON-1 | **Tutorial de primer uso** de 6 pasos cortos: bienvenida; dibujá tu espacio; agregá y mové plantas; leé el mapa (marca de atención, macetas, buenas parejas); sol y clima (elegir ciudad o compartir ubicación); logros y descuentos de Plus. | P0 |
| ON-2 | Cada paso tiene una imagen, opción de saltear, atrás/siguiente e indicador de progreso. El paso de ubicación se puede completar dentro del tutorial. | P0 |
| ON-3 | El tutorial se puede volver a ver desde Perfil → Ajustes. | P0 |
| ON-4 | La app real arranca con un primer espacio vacío y guiado, no con datos de ejemplo. | P0 |

### 7.2 Espacios

| ID | Requisito | Prioridad |
|---|---|---|
| SP-1 | Crear un espacio con **nombre**, **tipo** (jardín / cosecha), **ancho** y **largo** en metros. | P0 |
| SP-2 | **Profundidad de suelo** opcional en cm (canteros elevados, jardineras). | P0 |
| SP-3 | Varios espacios por usuario, se cambian desde el chip del título (límites por plan en 7.10). | P0 |
| SP-4 | Editar medidas después de crear; las plantas que quedan afuera se marcan, nunca se borran sin avisar. | P0 |
| SP-5 | Obstáculos fijos en la grilla (paredes, árboles, caminos, solados). | P1 |
| SP-6 | Formas no rectangulares (en L, polígonos). | P1 |

### 7.3 Sandbox

**Modelo:** una grilla en unidades reales. Celda por defecto = **10 cm** (25 cm en espacios muy grandes). El sandbox respeta la **proporción exacta** del espacio. Las posiciones se guardan en centímetros, así que cambiar la grilla nunca rompe un diseño.

**Las plantas son superficies**, dibujadas como elipses del tamaño de su **ancho y largo adultos**, con el color propio de la planta.

| ID | Requisito | Prioridad |
|---|---|---|
| SB-1 | Dibujar a escala con grilla, reglas en metros e indicador de norte. | P0 |
| SB-2 | Agregar una planta desde un catálogo con búsqueda (panel inferior); se ubica en el primer lugar libre. | P0 |
| SB-3 | Ancho, largo y alto adultos por defecto; el usuario puede cambiar los tres. | P0 |
| SB-4 | Arrastrar para mover (se ajusta a la grilla), flechas del teclado para mover de a poco, duplicar, quitar, deshacer. | P0 |
| SB-5 | **Chequeo de interacciones** dentro de un radio de influencia: **amontonamiento** (las copas se pisan de adultas), **pH de suelo incompatible**, **invasión** (raíces que se expanden), **competencia** (por ejemplo, el hinojo) y **buenas parejas**. Cada aviso muestra el motivo y el nivel de confianza. | P0 |
| SB-6 | **Marcas claras:** una planta con un problema muestra una **marca de atención (!)** en su borde; las buenas parejas se unen con una línea verde punteada; la planta seleccionada tiene un anillo sólido. Debajo del sandbox hay referencias que explican cada marca. | P0 |
| SB-7 | **Macetas:** cualquier planta puede estar "en el suelo" o "en maceta", con su propio diámetro. Se dibuja como el borde de una maceta vista desde arriba. La maceta separa raíces y suelo, así que no aplican los avisos de invasión, pH ni competencia de raíces; sí aplican amontonamiento y sombra. Los avisos de raíz ofrecen un botón **"Poner en maceta"**. Avisa si la maceta parece chica para la planta. | P0 |
| SB-8 | Dato de **tierra libre** (% y m²) y cantidad de problemas debajo del sandbox. | P0 |
| SB-9 | Funciona sin conexión; sincroniza al volver. | P1 |

### 7.4 Sol y sombra

| ID | Requisito | Prioridad |
|---|---|---|
| SU-1 | **Ubicación:** el usuario comparte su ubicación GPS o elige una ciudad. Saphi obtiene hemisferio, latitud, ángulo del sol, clima local y suelo probable. | P0 |
| SU-2 | La **elección manual de hemisferio** (Sur / Norte) sigue disponible para quien no quiera compartir su ubicación. | P0 |
| SU-3 | **Chequeo de sombra:** largo de la sombra al mediodía solar = altura de la planta ÷ tan(elevación del sol), para hoy, pleno invierno o pleno verano. Avisa cuando una planta alta le hace sombra a una que necesita sol pleno. | P1 |
| SU-4 | **Capa de sombras al mediodía:** opción que dibuja la sombra de cada planta para la estación elegida. | P1 |
| SU-5 | **Estudio de sol:** fotos del espacio desde el mismo punto a las 08:00, 13:00 y 19:00 (con la de las 13:00 alcanza para empezar). El MVP las guarda; el análisis que ubica luz y sombra en la grilla es P2. | P1 / P2 |

### 7.5 Catálogo de plantas

| ID | Requisito | Prioridad |
|---|---|---|
| PC-1 | Catálogo curado de plantas ornamentales y comestibles (meta: 150 especies para el MVP). | P0 |
| PC-2 | Por planta: nombres comunes (es/en), nombre científico, familia, altura y diámetro adultos (como rangos), distancia de plantación, sol, agua, rango de pH, ciclo de vida, meses de siembra por hemisferio, días a cosecha, rareza, color, rasgos climáticos (`lowFruit`, `heatBolt`, `frostTender`) y marcas (`invasive`, `allelopathic`, `pollinator`). | P0 |
| PC-3 | Relaciones entre pares: planta A ↔ planta B, buena o mala, motivo, confianza y fuente. | P0 |
| PC-4 | Plantas personalizadas creadas por el usuario (privadas). | P1 |
| PC-5 | Proceso de importación desde fuentes externas, con normalización y fuente por campo. | P1 |
| PC-6 | **Catálogo del MVP para Mendoza:** unas 60 especies tomadas de lo que más venden los viveros locales (lista reunida durante la validación), cada una con pros, contras y datos completos. | P0 |
| PC-7 | **Etiqueta "Nativa"** y **consumo de agua del 1 al 10** por especie; consumo promedio visible por espacio. Las nativas suman puntos extra en la colección. No se empujan nativas silvestres como opción de jardín. | P0 |
| PC-8 | Marca de **invasora en Argentina** (por ejemplo, *Gleditsia triacanthos* "acacia negra", *Robinia pseudoacacia* "acacia blanca"): al ubicarla siempre aparece un aviso crítico con una alternativa no invasora. | P0 |

Fuentes candidatas (verificar licencias): USDA PLANTS, Perenual, Permapeople, Trefle, Wikidata, guías regionales de extensión. Las relaciones entre pares requieren **curación manual**: no existe un único conjunto de datos confiable. Guardar rangos (mín./máx.), no valores únicos.

### 7.6 Cuidado, clima y siembra

| ID | Requisito | Prioridad |
|---|---|---|
| CR-1 | Tareas de cuidado generadas por planta (riego, abono, poda, cosecha) según el catálogo y la estación. | P1 |
| CR-2 | Tareas en Inicio y el próximo recordatorio debajo del sandbox; notificaciones push web. | P1 |
| CR-3 | Marcar una tarea como hecha → suma a la racha semanal. | P1 |
| CR-4 | **Pronóstico de 5 días** en Inicio: día, ícono, máxima/mínima, lluvia en mm o "Seco". Nada más en la franja. | **P0** |
| CR-5 | **Cada día se puede tocar** y abre un panel con: resumen, máxima, mínima, lluvia y probabilidad, la alerta explicada y qué hacer con tus plantas ese día. | **P0** |
| CR-6 | **Los días con alerta** se marcan en ámbar **y** con la etiqueta de la alerta ("Granizo", "Zonda", "Helada", "Lluvia", "Calor"), para que el color nunca sea la única señal. El panel explica el porqué. | **P0** |
| CR-7 | **Precauciones climáticas** por planta: granizo → cubrir la huerta y las plantas de hoja blanda con tela antigranizo o media sombra; Zonda → regar temprano y resguardar las plantas jóvenes y en maceta; helada → cubrir los cultivos sensibles; lluvia fuerte → levantar del suelo mojado los frutos bajos; calor → media sombra para lechuga y hortensia. En Mendoza las alertas climáticas son **P0**. | **P0** |
| CR-7a | **Tipo de riego** por espacio: "Manguera" o "Goteo"; las tareas de riego lo usan. El riego por turno se suma si las entrevistas muestran que es común. | P0 |
| CR-8 | La lluvia reduce la recomendación de riego ("Regá menos esta semana: vienen unos 44 mm de lluvia"). Saphi solo dice **no regar** cuando un sensor de suelo confirma que la tierra está húmeda (P3). | P1 |
| CR-9 | Los pronósticos cambian seguido (por ejemplo, en años de El Niño). Las precauciones se revisan cada mañana; los días 4 y 5 aclaran que son menos seguros. | P1 |
| CR-10 | **Sembrá este mes:** cultivos para sembrar ahora según el hemisferio del usuario. Al tocar uno se abre el catálogo con ese cultivo. | P1 |
| CR-11 | **Línea de tiempo de cosecha:** por cultivo, días desde la siembra, ventana esperada, barra de progreso y "Listo". Los emojis aparecen solo acá y en las fichas de plantas de cosecha. | P1 |
| CR-12 | Sugerencias de rotación de cultivos para la próxima temporada. | P2 |

### 7.7 Asesor de plantación con IA

El asesor responde preguntas como "Con lo que ya tengo, ¿qué me conviene plantar acá?". Está **limitado a propósito**: nunca inventa datos.

| ID | Requisito | Prioridad |
|---|---|---|
| AD-1 | Chat dentro de cada espacio. Las respuestas usan los datos reales del espacio: tamaño, tierra libre, plantas, macetas, sol y sombra, ubicación, suelo, estación y pronóstico. | P1 |
| AD-2 | **Proceso:** (1) reunir el contexto desde la base de datos y las APIs; (2) el modelo propone candidatas **solo del catálogo**; (3) cada candidata se ubica en un lugar libre y pasa por el **mismo motor de reglas** que las ubicaciones manuales; (4) al usuario solo le llegan las candidatas sin problemas (o con una solución indicada, como una maceta). | P1 |
| AD-3 | Cada afirmación cita su fuente (catálogo, mapa de suelos, pronóstico, regla) y aclara cuando es una estimación. Las preguntas fuera de jardinería se rechazan. | P1 |
| AD-4 | Cada sugerencia tiene un botón "Agregar a mi espacio" que la ubica en la grilla. | P1 |
| AD-5 | Límites de uso por plan; el proveedor del modelo se puede cambiar. | P1 |

### 7.8 Datos de suelo

| ID | Requisito | Prioridad |
|---|---|---|
| SO-1 | pH, textura y carbono orgánico probables para las coordenadas del usuario. Fuentes: mapas de suelos del **INTA** (Argentina) e **ISRIC SoilGrids** (global, grilla de ~250 m). Verificar licencias y condiciones de las APIs. | P1 |
| SO-2 | Los mapas de suelos son estimaciones de la zona, no del patio del usuario: se muestran como "pH probable". Una medición con kit casero cargada por el usuario tiene prioridad. | P1 |
| SO-3 | El pH del suelo alimenta los chequeos de pH y al asesor. En Mendoza (suelo mayormente alcalino), las plantas de suelo ácido plantadas en el suelo reciben el aviso "Suelo alcalino" con la opción de pasarlas a maceta en un toque. | P1 |

### 7.9 Perfil y gamificación

| ID | Requisito | Prioridad |
|---|---|---|
| GM-1 | **Nivel** según puntos de biodiversidad (Plantín → Brote → Cultivador → Jardinero → Paisajista → Maestro jardinero). | P1 |
| GM-2 | **Colección de plantas:** cada especie plantada queda "descubierta"; las no descubiertas muestran cuántos puntos valen. | P0 |
| GM-3 | **Racha semanal de cuidado** (semanal, para no castigar la vida normal). | P1 |
| GM-4 | **Puntaje de biodiversidad:** puntos por especie según rareza, más un extra por familia botánica. | P1 |
| GM-5 | **Logros por niveles (I / II / III)** con barra de progreso: Coleccionista (5/15/30 especies), Constancia (4/12/26 semanas), Buenos vecinos (1/3/5 espacios sin problemas), Amigo de los polinizadores (3/5/8 especies en un espacio), Lector de sol (1/3/9 fotos), Previsor del clima (1/10/25 precauciones), Cosechador (1/10/50 cosechas). | P1 |
| GM-6 | **Logros Plus** (Buenos vecinos, Lector de sol, Previsor del clima): cada nivel nuevo da **20% de descuento en el mes siguiente de Plus**, aplicado automáticamente, un descuento por mes. Ver [ADR 0001](adr/0001-plus-achievement-discounts.md). | P2 |
| GM-7 | Los logros gratuitos dan premios en el nivel III: descuento en un sensor de suelo o en el kit de riego, un mes de Plus. | P3 |
| GM-8 | Sin rankings ni funciones sociales. | — |

### 7.10 Planes y límites

| ID | Requisito | Prioridad |
|---|---|---|
| PL-1 | **Beta / MVP:** todo gratis, espacios ilimitados. | P0 |
| PL-2 | **Plan gratuito (después de la beta):** un espacio por cuenta verificada (email y, opcionalmente, teléfono). No por IP: la IP la comparten hogares, oficinas y operadoras móviles, y cambia seguido. | P2 |
| PL-3 | **Saphi Plus** (opcional, más adelante; precio previsto US$5/mes): espacios ilimitados, asesor con IA, análisis del estudio de sol, renders con IA y logros Plus. La app principal sigue siendo gratis. | P2 |
| PL-4 | **Mapa de viveros (próxima función grande después del MVP):** viveros y florerías de Mendoza, cargados a mano y guardados a largo plazo. Los viveros pagan para aparecer más arriba **solo cuando el usuario busca un tipo de planta que venden**, siempre ponderado por cercanía y marcado como "Destacado". El pago nunca cambia las recomendaciones de plantas ([ADR 0002](adr/0002-paid-placement-only-in-shop-map.md)). | P2 |
| PL-5 | **QR en el vivero:** un QR en el mostrador que abre Saphi, primero como canal de validación. | P1 |

### 7.11 Temas visuales

| ID | Requisito | Prioridad |
|---|---|---|
| TH-1 | Glassmorphism: paneles translúcidos con desenfoque sobre un fondo suave de "luz entre hojas". | P0 |
| TH-2 | **Tema de día / noche** según la hora local (amanecer y atardecer si se conoce la ubicación). Opción manual Automático / Día / Noche en ajustes. | P0 |
| TH-3 | **El tema de noche está diseñado, no invertido:** fondo verde casi negro, tonos fríos de luz de luna, rellenos de plantas más visibles y bordes de maceta neutros (sin marrón terracota de noche). | P0 |
| TH-4 | Contraste WCAG AA en ambos temas; respetar `prefers-reduced-motion`. | P0 |

### 7.12 Visualización del jardín con IA (P2)

| ID | Requisito | Prioridad |
|---|---|---|
| AI-1 | El usuario fotografía el espacio real y marca sus 4 esquinas. | P2 |
| AI-2 | Se genera un render realista del plan sobre la foto, marcado como "ilustrativo". | P2 |
| AI-3 | Opcional: control de tiempo (al plantar, a los 3 meses, adulto). | P2 |
| AI-4 | Opcional: identificación de plantas desde una foto. | P2 |

### 7.13 Sensores y riego (P3)

| ID | Requisito | Prioridad |
|---|---|---|
| HW-1 | Sensor de suelo Saphi: humedad, temperatura, luz; más adelante conductividad y nutrientes. | P3 |
| HW-2 | Asignar un sensor a una zona; "Agua – – –" pasa a mostrar datos en vivo. | P3 |
| HW-3 | API de ingreso de datos de dispositivos (MQTT o HTTPS) con tokens por dispositivo. | P3 |
| HW-4 | Integraciones con controladores de riego existentes (candidatos: Home Assistant, OpenSprinkler; a investigar). | P3 |
| HW-5 | Reglas de riego ("regar la zona B cuando la humedad baje de 30%") y recomendación de "no regar" respaldada por el sensor. | P3 |
| HW-6 | Tienda dentro de la app para sensores y kits. | P3 |

## 8. Requisitos no funcionales

| Área | Requisito |
|---|---|
| Plataforma | PWA instalable; Safari móvil y Chrome Android. |
| Rendimiento | Sandbox a 60 fps con 200 plantas en un celular de gama media; primera carga < 3 s en 4G. |
| Sin conexión | Edición del sandbox sin conexión (P1); sincronización con "gana la última escritura" y aviso de conflicto. |
| Idiomas | **Español rioplatense primero** (voseo), con textos preparados para traducir; inglés más adelante; unidades métricas. |
| Accesibilidad | WCAG 2.2 AA. Las plantas se pueden enfocar con teclado; cada marca tiene su equivalente en texto; el color nunca es la única señal. |
| Privacidad | Guardar lo mínimo: email, ciudad (no la ubicación GPS exacta) y los espacios del usuario. Métricas de uso limitadas a saber si la gente la usa de verdad (sesiones, semanas en que vuelve, espacios creados), respetuosas de la privacidad y sin publicidad. Fotos borradas después del análisis salvo que el usuario las guarde. No se venden ni comparten datos de usuarios. |
| Seguridad | **Ingreso sin contraseña:** un código de un solo uso enviado por email y, después, una cookie de sesión segura (HTTP-only). Sin contraseñas. El progreso de logros se calcula en el servidor. Tokens de sensores por dispositivo. |

## 9. Arquitectura técnica (propuesta)

### 9.1 Stack

| Capa | Elección | Motivo |
|---|---|---|
| Frontend | React + TypeScript + Vite, PWA | Cliente muy interactivo. |
| Sandbox | SVG primero; Canvas si hace falta | Simple, accesible, fácil de detectar toques. |
| Estilos | Tailwind + design tokens (día/noche) | Temas basados en tokens. |
| Backend | Django + Django REST Framework (o Django Ninja) | El fundador quiere aprender Django; el admin es ideal para curar el catálogo. |
| Base de datos | PostgreSQL (Supabase o Neon) + JSONB | Ver 9.2. |
| Tareas en segundo plano | Celery o Django-Q + Redis | Recordatorios, importaciones, pronósticos, IA. |
| Almacenamiento | Compatible con S3 (Supabase Storage / Cloudflare R2) | Imágenes y fotos. |
| Clima | Open-Meteo | Gratis, sin clave, global. |
| Suelo | Mapas del INTA, ISRIC SoilGrids | Ver 7.8. |
| IA | LLM detrás de un servicio del backend, con llamadas a herramientas que usan el motor de reglas | Ver 7.7. |

### 9.2 PostgreSQL en lugar de MongoDB Atlas

- El ORM, las migraciones, el admin y la autenticación de Django están hechos para bases relacionales; el backend de MongoDB para Django es más nuevo y funciona con menos apps de terceros.
- Los datos son relacionales: usuarios → espacios → ubicaciones → plantas → relaciones entre pares.
- Los atributos flexibles entran en JSONB.
- Solo las series de tiempo de los sensores (P3) tienen mucho volumen; TimescaleDB (una extensión de Postgres) las cubre.

### 9.3 Modelo de datos principal (borrador)

```
User(id, email, locale, units, theme_mode, city, lat?, lon?, hemisphere, timezone, tutorial_done)

Space(id, user_id, name, kind[garden|harvest], width_cm, length_cm, depth_cm?,
      north_angle_deg?, cell_size_cm)

Placement(id, space_id, plant_id, x_cm, y_cm, spread_x_cm, spread_y_cm, height_cm,
          pot_diameter_cm?, count?, planted_at?, notes)

Plant(id, scientific_name, common_names{es,en}, family, height_cm_min/max,
      spread_cm_min/max, spacing_cm, sun, water, ph_min, ph_max, lifecycle,
      sowing_months_south[], days_to_harvest_min/max, rarity, color,
      traits[], flags[], sources{})

PairRelation(plant_a_id, plant_b_id, kind[good|bad], reason, confidence, source)

SoilEstimate(lat_round, lon_round, ph, texture, organic_carbon, source, fetched_at)
SoilReading(space_id, ph, measured_at)                          -- kit casero del usuario

CareTask(id, placement_id, kind, due_at, done_at?)
Forecast(location_key, day, hi, lo, rain_mm, chance, fetched_at)
Precaution(id, user_id, day, kind, plant_ids[], done_at?)

AchievementTier(user_id, chain, tier, earned_at)
PendingDiscount(subscription_id, percent, source_tier, applies_to_period)

SunStudyPhoto(space_id, slot[08|13|19], url, taken_at)          -- P1/P2
AdvisorMessage(space_id, role, content, citations[], created_at) -- P1
Device / Reading                                                 -- P3
```

### 9.4 Estructura del repositorio

```
saphi/
├── apps/web/          # PWA en React
├── apps/api/          # Django
│   ├── accounts/  spaces/  catalog/  care/  weather/  soil/
│   ├── advisor/       # proceso de IA (las herramientas llaman al motor de reglas)
│   └── gamification/  billing/
├── packages/rules/    # motor de reglas puro (amontonamiento, pH, invasión, sombra, macetas), replicado en TS
├── prototype/
└── docs/  (PRD, ADRs)
```

El **motor de reglas es código puro**, sin dependencias de frameworks: el sandbox, el asesor y los tests usan las mismas funciones.

## 10. Hoja de ruta

| Fase | Contenido | Criterio de salida |
|---|---|---|
| **0 — Prototipo** ✅ | Prototipo navegable en español rioplatense, adaptado a Mendoza. | — |
| **0b — Validación (2 semanas)** | Entrevistas en Mendoza con el prototipo: 10 principiantes y 5 viveros ([guía](validation/interview-guide.md)); conseguir la lista de plantas del vivero. | Se sigue si ≥ 6 de 10 principiantes lo usarían para su propio espacio **y** ≥ 2 viveros aceptan el QR en el mostrador. Si no, queda como proyecto para aprender. |
| **1 — MVP (P0)** | Ingreso sin contraseña, espacios, sandbox con macetas y chequeos, catálogo de Mendoza (~60), ubicación/hemisferio, tipo de riego, alertas climáticas (granizo, Zonda, helada), siembra del mes, tutorial, colección, temas, PWA. Arranca con ~5 a 10 cuentas. | **5 a 10 personas que no nos conocen** la usan y vuelven solas al menos 3 de 4 semanas. |
| **2 — Retención (P1)** | Tareas + push, línea de tiempo de cosecha, racha, logros, sombra, datos de suelo, QR en viveros, asesor con IA. | Retención en la semana 4 ≥ 25%. |
| **3 — Mapa de viveros + Plus (P2)** | Mapa de viveros pago (ADR 0002), Saphi Plus opcional con descuentos automáticos (ADR 0001), análisis del estudio de sol, renders. | Primeros viveros que pagan. |
| **4 — Hardware (P3)** | Piloto de sensores, API de datos, integraciones de riego, tienda. | 10 sensores piloto funcionando durante un mes. |

## 11. Métricas de éxito

- **Activación:** % que crea un espacio y ubica ≥ 5 plantas en la primera sesión.
- **Tutorial completado** y tiempo hasta el primer diseño (meta < 5 min).
- **Retención:** semana 1 y semana 4.
- **Tasa de corrección:** % de avisos resueltos (planta movida, achicada o pasada a maceta) frente a ignorados.
- **Precauciones cumplidas:** % de precauciones climáticas marcadas como hechas.
- **Aceptación del asesor:** % de sugerencias del asesor agregadas a un espacio.
- **Conversión y bajas de Plus**, y descuento promedio por usuario pago.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Calidad y licencias de los datos de plantas y pares. | Curación manual para el MVP; fuente por campo; etiquetas de confianza. |
| El asesor con IA afirma datos incorrectos. | Candidatas solo del catálogo, validación con el motor de reglas, citas y rechazo de temas fuera de alcance. |
| Los mapas de suelo no coinciden con el patio real. | Texto de "pH probable"; prioridad a la medición con kit casero. |
| Sandbox demasiado complejo en una pantalla chica. | Tutorial, referencias del mapa, pruebas con paisajistas. |
| Los descuentos reducen los ingresos. | Un solo descuento de 20% por mes, logros calculados en el servidor (ADR 0001). |
| Crecimiento descontrolado del alcance. | Fases con criterio de salida; P2/P3 solo después de las métricas del MVP. |
| El hardware es otro negocio. | Validar primero con sensores comerciales e integraciones. |
| Tiempo disponible del fundador. | MVP chico; validar temprano con usuarios reales. |

## 13. Preguntas abiertas

1. ¿Nombre final de la marca: **Saphi**?
2. ¿Qué ~60 especies entran en el catálogo de Mendoza? (pendiente de la lista del vivero)
3. ¿El riego por turno es lo bastante común entre principiantes como para incluirlo en el MVP?
4. Precio del mapa de viveros (después de la validación).
5. Precio de Plus en pesos, si finalmente se lanza.

## 14. Glosario

- **Espacio:** un jardín o una huerta con medidas reales.
- **Sandbox:** la grilla interactiva a escala de un espacio.
- **Ubicación (placement):** una planta en una posición de un espacio, con su propio tamaño, opcionalmente en maceta.
- **Superficie:** el área que cubre una planta en su tamaño adulto.
- **Relación entre pares:** una interacción conocida, buena o mala, entre dos especies.
- **Motor de reglas:** el código compartido que verifica amontonamiento, pH, invasión, competencia y sombra.
- **Logro Plus:** un logro que da 20% de descuento en el mes siguiente de Saphi Plus.
