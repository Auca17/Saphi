# Notas crudas — Wave 1 (Mercado)

**Fase:** 3 — Investigación de mercado (Fast Track)
**Proyecto:** saphi-startup
**Fecha:** 2026-11-20
**Modo:** Investigación web (WebSearch/WebFetch). 17 búsquedas en Wave 1 + 2 fetches (1 fallido).

---

## A1 — Tamaño de mercado y economía

### Global (todas Tier 3: editoriales de "market research" de baja reputación, definiciones dispares)
- Home gardening (amplio, productos): USD 15,78 mil M en 2025, CAGR 5,92 % 2025-2034 (Custom Market Insights vía GlobeNewswire, mar-2025). Tier 3.
- "Smart gardening apps": USD 2,5 mil M en 2025, CAGR 17 % a 2033 (Future Data Stats). Tier 3, probablemente incluye hardware. Baja confianza.
- Vegetable garden planner software: USD 140 M en 2025, CAGR 5,5 % (Intel Market Research) vs. USD 846,3 M, CAGR 5,9 % (Wise Guy Reports). Diferencia 6x → definiciones incompatibles. Baja confianza.
- Plant identification apps: ~USD 500 M en 2025, CAGR 9,7-15 % (Market Research Forecast). Tier 3.
- Proxy más sólido de ingresos de apps: PictureThis sola factura ~USD 6-9 M/mes (estimaciones AppSprint, Screensdesign, Adapty; Appfigures reportó >USD 13 M netos en mayo-2022). Tier 2-3.
- EE.UU. gardening (productos): USD 22 mil M, CAGR ~4,5 % 2025-30 (MarkNtel). Tier 3.

### Argentina — apps
- Ingresos totales de apps Argentina 2022: €562,8 M; compras in-app €128,1 M; apps pagas €20,5 M; publicidad €414,2 M (Statista, es.statista.com). Tier 2. **Dato de >18 meses.** Implica que ~74 % del ingreso de apps en Argentina es publicidad, no pago del usuario.
- Statista (comentario): inflación y volatilidad cambiaria vuelven al consumidor más cauto con compras in-app y suscripciones. Tier 2, cualitativo.
- Internet: 41,2 M usuarios (90,1 %) ene-2025; 41,6 M (90,6 %) fin-2025 (DataReportal Digital 2025/2026). Tier 2.
- Android 86,1 % / iOS 13,9 % del móvil, jun-2026 (StatCounter). Tier 2. Relevante: PWA en Android es viable; iOS minoritario.
- 79 % de argentinos usa pagos digitales (Mastercard). Tier 2. Mercado Pago entre las apps más descargadas.
- RevenueCat SOSA 2025: LATAM muestra conversión de trial más variable; apps de precio bajo convierten descarga→trial 4,3 % (mediana) vs 9,8 % alto precio. Tier 2. Sin dato específico LATAM/categoría (detrás del PDF).
- DATA GAP: disposición a pagar por apps de jardinería en Argentina. No hay dato. Llenar con entrevistas.

### Argentina — viveros / retail
- SENASA registraba 717 viveros ornamentales productores, estructura familiar, concentrados en Buenos Aires (La Nación, ~2018). Tier 2, desactualizado. Son productores, no necesariamente minoristas.
- Garden centers en Argentina: 3.046 (jun-2026), 43,2 % en Prov. Buenos Aires (poidata.io, vendor de POI). Tier 3. Fetch directo devolvió 403; dato solo del snippet.
- Relevamiento Vivero 2024/2025 (MAGyP): es forestal, no ornamental. No sirve.
- DATA GAP: facturación del sector ornamental minorista; cantidad de viveros en Mendoza; gasto publicitario de un vivero. Llenar: relevamiento en Google Maps ("vivero" en Gran Mendoza) + 5 entrevistas a viveros.
- Contexto de consumo Mendoza: comercio entre los más golpeados; pymes perdieron 10 % del empleo en 1S-2025; consumo de frutas y verduras cayó 40-50 % (jun-2026); vino en mínimo histórico 15,7 L/persona 2025 (Sitio Andino, Los Andes, AP). Tier 2. Sin dato específico de viveros.

### Mendoza — demanda de usuarios
- Provincia: 652.184 hogares (Censo 2022, vía Fundación Tejido Urbano); ~600 mil relevados según Los Andes. Tier 1-2.
- Gran Mendoza: 1.273.144 habitantes (Fundación Metropolitana). 86,0 % de viviendas son casas, 12,6 % departamentos (DEIE, ECV 2022). Tier 1.
- DATA GAP: hogares con patio/jardín. No existe en resultados del Censo; REDATAM podría tenerlo. Proxy: "casa" (86 %).
- Huertas ProHuerta en Mendoza: ~10.000 por temporada (coordinación regional ProHuerta Mendoza-San Juan, El Sol, nov-2020, act. 2023). Tier 2. Población objetivo: inseguridad alimentaria, no el segmento de Saphi.

### Economía unitaria (benchmarks)
- Precios de competidores (Wave 2): US$ 25-48/año o US$ 4,99-9,99/mes.
- DATA GAP: CAC de apps de jardinería en LATAM; churn. Sin datos públicos.

## A2 — Tendencias y timing
- Pandemia: aumento de demanda de huerta y semillas en Mendoza/San Juan y Neuquén (ProHuerta, Río Negro). Tier 2. Tendencia 2020-2021; sin datos de que se sostenga.
- ProHuerta nacional: convenio INTA-Desarrollo Social terminó 29-feb-2024; programa discontinuado abr-2024 (proyecto de ley 1438-D-2024; Bichos de Campo). Cifras: 455.000-600.000 huertas beneficiarias. Tier 1-2. Implicación doble: vacío de asistencia técnica gratuita (oportunidad) y menos material actualizado (también menos competencia institucional).
- PBA lanzó programa provincial de huertas urbanas 2024-2025. Tier 1.
- Granizo: Mendoza tiene algunas de las tormentas de granizo más severas del mundo; especialistas ligan calentamiento global a más granizo grande (Los Andes, ene-2026). Temporada primavera-verano. Granizo muy localizado (100 celdas → 3 distritos). Tier 2. DATA GAP: frecuencia anual cuantitativa.
- Heladas tardías: promedio 17.580 ha afectadas/año (últimos 6 años) (Gobierno de Mendoza). Tier 1. Agrícola, no doméstico.
- Zonda: frecuencia poco estudiada (FCA-UNCuyo 2004). Tier 1, antiguo.
- Herramientas públicas: radar de la DACC (web, colores naranja/rojo = granizo), alertas SMN por departamento. No se encontró app oficial dedicada. Tier 1.
- IA: identificación de plantas (PictureThis, Planta "AI") ya es commodity. Inversión: Greg USD 5,4 M seed (2021); no se encontraron rondas 2025-26 en el nicho → inversión estancada [Opinion].

## A3 — Regulatorio (breve)
- Ley 25.326 (2000) sigue vigente en 2026 (Diario Judicial, jul-2026). Adecuación UE. Tier 1-2.
- AAIP: Res. 179/2025 sobre infracciones. Varios proyectos de reforma (2968-D-2025 perfilamiento y portabilidad; 3540-D-2025 transparencia algorítmica; 2023 proyecto integral). Ninguno sancionado según resultados.
- Implicación: inscripción de bases de datos ante la AAIP (obligación de la ley vigente [Data, conocimiento general; no verificado en esta búsqueda]); consentimiento informado; ubicación aproximada es dato personal. Riesgo regulatorio: Bajo.

## Fallas de búsqueda
- poidata.io (403). Sin dato de viveros Mendoza. Sin WTP Argentina. Sin frecuencia de granizo.
