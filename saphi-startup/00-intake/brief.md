# Brief de entrada

**Fase:** 1 — Entrevista (Fast Track)
**Proyecto:** saphi-startup
**Fecha:** 2026-11-20
**Confianza:** Media (basado en la conversación con el fundador; faltan las preguntas difíciles)

---

## La idea

- **Problema:** a los principiantes les cuesta imaginar su jardín o huerta, saber qué plantas conviven (se pisan, distinto pH, invasoras), evitar la sombra y sostener el cuidado frente al clima. En Mendoza el clima es extremo: granizo, viento Zonda, heladas tardías, riego por turno o manguera y suelo alcalino.
- **Solución:** app web mobile-first (PWA) con un sandbox a escala real, chequeos entre plantas, macetas, sol y sombra, alertas climáticas con precauciones por planta, "Sembrá este mes", línea de tiempo de cosecha, colección de plantas y logros.
- **Origen:** idea propia del fundador, que además quiere aprender Django.
- **Trabajo existente:** prototipo navegable en español adaptado a Mendoza (https://claude.ai/artifact/Q6LCHyEBq3khP7uZvdvwQU), PRD v0.3 (`docs/PRD.es.md`), ADR 0001 y 0002, guía de entrevistas (`docs/validation/interview-guide.md`).

## El fundador

- Estudiante universitario, fundador solo [Asumido: no hay cofundadores mencionados].
- Tiempo: 8 a 16 horas por semana durante un mes y medio, según la facultad, siempre que se valide el dolor.
- Otros proyectos: Audara (en validación con estudiantes, recién reconstruido) y Safi.
- Experiencia: SQL, MongoDB Atlas; quiere aprender Django.
- Presupuesto: no informado [pendiente].

## El mercado

- **Cliente ideal:** principiante en jardinería con poco tiempo, que vive en Mendoza, con patio, balcón o terraza.
- **Segmento futuro:** paisajistas (plan Pro).
- **Fuera de alcance:** producción comercial y agrónomos.
- **Alternativas actuales:** preguntarle al del vivero, Google, conocidos [Asumido; se valida en entrevistas].
- **Geografía:** Mendoza primero, después el resto de Argentina y, a largo plazo, otros países.

## El negocio

- **Gratis para el usuario.**
- **Ingreso futuro:** mapa de viveros y florerías donde los viveros pagan para aparecer más arriba solo al buscar ese tipo de planta, ponderado por cercanía (ADR 0002).
- **Opcional, más adelante:** Saphi Plus (US$5/mes) con descuentos por logros (ADR 0001); sensores de humedad.
- **Éxito a 6 semanas:** 6 de 10 principiantes dicen que lo usarían y 2 viveros aceptan un QR. Después del MVP: 5 a 10 personas desconocidas que vuelven solas 3 de 4 semanas.

## Restricciones

- Mobile-first, español rioplatense, sin explotación de datos, ingreso sin contraseña (código por email y cookie).
- Stack previsto: React + Django + PostgreSQL.

## Preguntas difíciles (respuestas del fundador, 2026-11-20)

1. **¿Por qué vos?** Vive en Mendoza; su padre sabe de plantas; tiene un posible tester herborista (suegro del padre de un amigo); visión de sumar sensores reutilizables y alianzas con empresas de riego. [Opinión] Ventaja moderada: acceso local y a conocimiento, sin experiencia propia en el rubro ni red de viveros todavía.
2. **Si Planta, PictureThis o Google agregan alertas de granizo para Mendoza:** "le mando una notificación por WhatsApp". [Opinión] Eso es un canal, no una defensa: también se puede copiar. La defensa real sería el dato local curado (catálogo de Cuyo, red de viveros, datos de sensores).
3. **Argumento más fuerte en contra:** la gente ya usa muchas apps; la diferenciación sería el conjunto (planificador, clima, mapa de viveros, sistema para viveros, alianzas de riego). [Opinión] El argumento más fuerte en contra es otro: mercado chico y monetización no probada, y querer hacer todo a la vez.
4. **¿Se lo mostraste a alguien?** Sí, a una persona (padre de un amigo): le encantó, pero no la usaría porque no le interesan las plantas. Todavía no habló con viveros.
5. **¿Qué te haría abandonarla?** No tener plata para sensores ni para el hosting. Plan de financiamiento: presentarla a fondos de capital de riesgo de Mendoza.

**Presupuesto propio:** no informado.

---

## Flags

**Red Flags:**
- Ninguno identificado todavía.

**Yellow Flags:**
- Fundador solo, con tiempo parcial y otros dos proyectos activos.
- Modelo de ingresos diferido: el usuario no paga y el mapa de viveros es posterior al MVP.
- Todavía no hubo conversaciones con clientes reales.

## Sources
- Conversación con el fundador (2026-11-18 a 2026-11-20); `docs/PRD.es.md`.
