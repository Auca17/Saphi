# Análisis de mercado

**Fase:** 3 — Investigación de mercado (Fast Track: Wave 1)
**Proyecto:** saphi-startup
**Fecha:** 2026-11-20
**Confianza:** Baja-Media (fuentes de tamaño global Tier 3; casi sin datos locales de viveros y disposición a pagar)

---

## Resumen ejecutivo

1. Los números globales de "apps de jardinería" no sirven para decidir: las estimaciones del mismo segmento difieren 6 veces (USD 140 M vs. 846 M) [Data, Tier 3].
2. Saphi no le cobra al usuario, así que su mercado real es **lo que los viveros pagarían por visibilidad**, no el mercado de apps.
3. Con esa lógica, Mendoza es chico: unos **US$ 40 mil/año** al 100 % de penetración, y unos **US$ 3-5 mil/año** de mercado capturable realista [Estimate].
4. El contexto juega a favor del producto (granizo severo, fin de ProHuerta nacional en 2024, 86 % de viviendas tipo casa en Gran Mendoza) y en contra del modelo de ingresos (consumo minorista en caída fuerte en Mendoza 2025-2026).
5. Conclusión: Mendoza funciona como **laboratorio de validación**, no como mercado que sostenga un negocio [Opinion].

## Tamaño de mercado

### Usuarios (Gran Mendoza)

| Paso | Valor | Base |
|---|---|---|
| Habitantes Gran Mendoza | 1.273.144 | [Data, Fundación Metropolitana, Censo 2022] |
| Hogares (÷ 3,13 personas/hogar provincial) | ~407.000 | [Estimate; 2.043.540 hab. / 652.184 hogares provinciales] |
| Hogares en casa (86 %) | ~350.000 | [Data, DEIE ECV 2022] |
| Principiantes interesados en usar una app (10 %) | **~35.000** | [Assumption: validar en entrevistas] |
| Usuarios activos alcanzables año 1 (1-3 %) | **350-1.000** | [Estimate] |

### Ingresos (el que paga es el vivero)

| Nivel | Cálculo | Resultado |
|---|---|---|
| TAM Argentina (listados de viveros) | 3.046 garden centers × US$ 25/mes × 12 | **~US$ 0,9 M/año** [Estimate; conteo de viveros: poidata.io, Tier 3; precio: Assumption] |
| SAM Mendoza | ~135 viveros (4,4 % de la población nacional) × US$ 25 × 12 | **~US$ 40 mil/año** [Estimate] |
| SOM año 1-2 | 10-15 viveros pagando | **US$ 3-4,5 mil/año** [Estimate] |
| Plus (complementario) | 1.000 usuarios × 2 % × US$ 3/mes × 12 | **~US$ 720/año** [Estimate; precio regional, no US$ 5] |

[Opinion] Aun a escala nacional con 15 % de viveros pagando, el ingreso por listados ronda **US$ 137 mil/año**. Alcanza para un proyecto rentable chico, no para una startup de capital de riesgo.

## Crecimiento y madurez

- Jardinería doméstica global: USD 15,8 mil M (2025), CAGR 5,9 % [Data, Custom Market Insights, Tier 3]. Mercado **maduro**.
- Apps de cuidado de plantas: la categoría ya tiene un ganador grande (PictureThis, ~US$ 6-9 M/mes estimados) [Data, Tier 3]. La identificación por IA es commodity.
- Argentina: el 74 % del ingreso de apps (2022) venía de publicidad y solo el 23 % de compras in-app (€128 M) [Data, Statista, Tier 2, >18 meses]. Esto confirma la decisión de no cobrarle al usuario.

## Economía unitaria (benchmarks)

- Precio de referencia de la competencia: **US$ 25-48/año** o US$ 4,99-9,99/mes (ver `competitor-landscape.md`) [Data].
- Conversión descarga→trial en apps baratas: mediana 4,3 %; LATAM con más variación [Data, RevenueCat 2025, Tier 2].
- DATA GAP: CAC, churn y precio que aceptaría un vivero mendocino. Se completa con 5 entrevistas a viveros.

## Timing: ¿por qué ahora?

**A favor**
- Granizo: Mendoza tiene algunas de las tormentas de granizo más severas del mundo, y se asocian a granizo más grande con el calentamiento [Data, Los Andes ene-2026, Tier 2].
- Heladas tardías: 17.580 ha afectadas por año en promedio [Data, Gobierno de Mendoza, Tier 1]. Son datos agrícolas, pero muestran que el riesgo es real.
- El radar DACC y el SMN avisan, pero **no dicen qué hacer con cada planta** [Data, mendoza.gov.ar].
- ProHuerta nacional terminó en abril de 2024 y dejó un vacío de asistencia técnica gratuita [Data, HCDN 1438-D-2024, Tier 1].
- 86 % Android, 90 % con internet, 79 % paga digital [Data, StatCounter/DataReportal/Mastercard, Tier 2]. La PWA es viable.

**En contra**
- Consumo en Mendoza: pymes de comercio perdieron 10 % del empleo en el primer semestre de 2025; frutas y verduras -40-50 % (jun-2026) [Data, Sitio Andino/Los Andes, Tier 2]. Los viveros podrían no tener presupuesto para publicidad.
- El boom de la huerta fue pandémico (2020-21); no hay evidencia de que siga [Data, ProHuerta; Opinion].

## Regulatorio

- Rige la **Ley 25.326** (2000); en 2026 sigue vigente y hay proyectos de reforma sin sancionar (2968-D-2025, 3540-D-2025) [Data, Tier 1-2].
- Mínimo para el lanzamiento: política de privacidad, consentimiento informado, inscripción de la base en el registro de la AAIP [Assumption: requisito de la ley vigente, confirmar en argentina.gob.ar/aaip] y tratar la ubicación como dato personal. Costo bajo y sin certificaciones.
- Riesgo regulatorio: **Bajo**.

## Beachhead y expansión

Gran Mendoza (~35 mil principiantes potenciales, ~85-135 viveros) → resto de Cuyo (San Juan comparte coordinación ProHuerta y riesgos climáticos) → Córdoba/PBA (PBA concentra 43 % de los viveros) [Estimate].

## Data gaps

1. Hogares con patio en Gran Mendoza (Censo 2022 REDATAM).
2. Cantidad real de viveros en Gran Mendoza (relevar en Google Maps).
3. Cuánto pagaría un vivero por visibilidad y cuánto gasta hoy en publicidad.
4. Disposición a pagar de usuarios argentinos por apps de jardinería.
5. Frecuencia anual de granizo por departamento (SMN/DACC).

## Conexiones estratégicas

- El vacío "alerta → acción por planta" no lo cubre ningún competidor ni el radar DACC (ver `competitor-landscape.md`, sección Brechas).
- El mapa de viveros compite contra Google Maps gratis (ver `competitor-landscape.md`, Riesgo de plataforma): el TAM de listados asume que el vivero ve valor extra.

---

## Flags

**Red Flags:**
- El mercado capturable en Mendoza (US$ 3-5 mil/año) no sostiene un negocio; incluso a nivel nacional el modelo de listados ronda US$ 0,1-0,9 M/año [Estimate].

**Yellow Flags:**
- Viveros mendocinos bajo presión de consumo 2025-2026: su presupuesto publicitario es dudoso.
- US$ 5/mes de Plus probablemente supera la disposición a pagar argentina; hace falta precio regional.
- El tamaño global depende de reportes Tier 3 contradictorios.

## Sources
- Censo 2022 / Fundación Tejido Urbano; Fundación Metropolitana (Tier 1-2)
- DEIE Mendoza, ECV 2022 (Tier 1)
- Statista Argentina App Outlook 2022 (Tier 2)
- DataReportal Digital 2025/2026 Argentina; StatCounter jun-2026; Mastercard (Tier 2)
- RevenueCat State of Subscription Apps 2025 (Tier 2)
- Custom Market Insights, Intel Market Research, Wise Guy Reports, Future Data Stats (Tier 3)
- poidata.io, garden centers Argentina jun-2026 (Tier 3)
- Los Andes, Sitio Andino, El Sol, Bichos de Campo, Gobierno de Mendoza, HCDN 1438-D-2024 (Tier 1-2)
- Diario Judicial jul-2026; AAIP Res. 179/2025 (Tier 1-2)
