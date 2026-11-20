# Diseño de experimentos (top 3)

**Fase:** 8 — Validación
**Proyecto:** saphi-startup
**Fecha:** 2026-11-20
**Confianza:** Media

---

## 1. ¿Los viveros pagan? (lo más importante)

- **Hipótesis:** al menos 3 de 10 viveros de Mendoza aceptan un piloto pago de catálogo + QR.
- **Cómo:** visitar 10 viveros con el prototipo en el celular. Usar las preguntas de vivero de `docs/validation/interview-guide.md` y al final hacer una oferta concreta: "Tu catálogo en Saphi + QR en el mostrador, 2 meses gratis y después ARS [equivalente a US$15–20]/mes". Pedir la lista de plantas que más venden.
- **Métrica:** cuántos dicen que sí al piloto **con precio**, no "me gusta".
- **Éxito:** ≥ 3 de 10 aceptan el piloto pago. **Fracaso:** < 2.
- **Tiempo y costo:** 2 semanas, US$0 más el transporte.

## 2. ¿Los principiantes lo quieren? (puerta falsa)

- **Hipótesis:** el QR en el mostrador y los grupos de jardinería de Mendoza traen interesados.
- **Cómo:** una página simple con "Planificá tu patio y recibí alertas de granizo para tus plantas" y un botón "Avisame por WhatsApp". Repartirla con el QR de 2 viveros y en 2 o 3 grupos de Facebook o Instagram de Mendoza. Sumar 10 entrevistas con la guía.
- **Métrica:** cantidad de personas que dejan su WhatsApp; respuestas de las entrevistas.
- **Éxito:** ≥ 30 personas en 2 semanas y ≥ 6 de 10 entrevistados que lo usarían para su espacio. **Fracaso:** < 10 personas.
- **Tiempo y costo:** 2 semanas, US$0–10.

## 3. ¿Las alertas sirven? (Mago de Oz)

- **Hipótesis:** quien recibe "qué hacer con tus plantas" ante granizo, Zonda o helada lo hace y quiere seguir recibiéndolo.
- **Cómo:** con las personas del experimento 2, mandar **a mano** por WhatsApp las precauciones de las próximas 3 alertas reales del SMN o la DACC, adaptadas a lo que cada uno tiene plantado. Sin construir nada.
- **Métrica:** % que responde o confirma que lo hizo; % que pide seguir.
- **Éxito:** ≥ 50% responde y ≥ 40% pide seguir. **Fracaso:** < 20% responde.
- **Tiempo y costo:** 3–4 semanas (depende del clima), US$0.

## Criterios para cortar o pivotear

| Si pasa esto… | …entonces |
|---|---|
| < 2 de 10 viveros aceptan el piloto pago | Abandonar el modelo B; probar ingresos por Plus o sensores, o dejarlo como proyecto de aprendizaje. |
| < 10 interesados en 2 semanas | El dolor no es tan fuerte: cortar o reducir a la variante C (solo clima). |
| < 20% responde a las alertas | Las alertas no generan hábito: repensar la propuesta de valor. |
| Nadie vuelve solo 3 de 4 semanas en el MVP | No construir más funciones; volver a entrevistar. |
| Audara consigue clientes pagos | Pausar Saphi sin culpa. |

---

## Flags

**Red Flags:**
- Ninguno nuevo.

**Yellow Flags:**
- El experimento 3 depende de que haya alertas climáticas en el período.

## Sources
- `06-validation/scorecard.md`, `docs/validation/interview-guide.md`.
