# PROYECTO DE INNOVACIÓN: SITA-IA
## Sistema Institucional de Tutorías y Alerta Temprana de Deserción
**Materia:** Fundamentos de Inteligencia Artificial (FIA - 3° Año)  
**Institución:** Universidad Champagnat — Facultad de Informática  
**Integrantes:** Joel Aisama · Bautista Navarro  
**Docente receptor:** `ampalmaj`  

---

### 1. SELECCIÓN DEL PROBLEMA LOCAL O CERCANO
* **Contexto:** 1.° Año de las carreras de Ingeniería en Sistemas de Información y Licenciatura en Informática de la Facultad de Informática (Universidad Champagnat).
* **El Problema:** La deserción universitaria en Argentina alcanza a casi 70 de cada 100 ingresantes a lo largo de la carrera, concentrándose mayoritariamente en el **primer cuatrimestre del primer año**.
* **Falla del método tradicional:** La detección actual es **tardía y reactiva**. Cuando un docente o preceptor nota que un estudiante no asiste a clase, el estudiante ya abandonó formalmente. Los datos (asistencia presencial, notas parciales, interacción en campus Moodle) se encuentran fragmentados en silos y no se cruzan a tiempo.
* **Oportunidad de la IA:** Identificar señales débiles multivariables dentro de las **primeras 6 semanas** de cursada para habilitar una intervención humana preventiva con al menos **4 semanas de anticipación**.

---

### 2. DEFINICIÓN DE USUARIOS, OBJETIVO, ALCANCE Y CRITERIOS DE ÉXITO

#### (a) Usuarios del Sistema:
1. **Usuarios Primarios (Operadores):**
   * **Tutores Docentes (Prof. Joel Aisama):** Reciben la bandeja de casos priorizada, analizan la explicabilidad del riesgo y realizan el acompañamiento personalizado.
   * **Coordinación Académica y Bienestar Estudiantil (Coord. Bautista Navarro):** Supervisa el padrón global, aprueba medidas institucionales (cambios de turno, becas) y autoriza la recalibración cuatrimestral del modelo.
2. **Usuario Aportante de Datos (Regla C1):**
   * **Docente de Cátedra:** Carga asistencia y calificaciones. **Tiene prohibido ver los puntajes de riesgo emitidos por la IA** para evitar sesgos de expectativa al corregir exámenes.
3. **Sujeto Afectado:**
   * **El Estudiante:** No opera el sistema. Recibe la propuesta de acompañamiento humano y decide libremente si acepta o rechaza la entrevista.

#### (b) Objetivo General:
Construir un sistema de alerta temprana basado en IA débil que consolide rastros académicos semanales, estime la propensión de abandono con alta explicabilidad y asista al tutor humano con guías de diálogo empático, con el fin de **reducir en un 15% la tasa de deserción estudiantil en el primer año**.

#### (c) Alcance: ¿Qué hace y qué NO hace la solución?
* **Lo que SÍ hace:**
  * Ingesta y cruza semanalmente 3 fuentes: asistencia presencial, notas de parciales/TPs y actividad en Campus Virtual.
  * Calcula un índice de riesgo (0 a 100) y extrae los **3 factores que más pesaron (XAI)**.
  * Prioriza y asigna una lista manejable con un tope operativo estricto de **máximo 15 casos por tutor a la semana**.
  * Utiliza la API de **Google AI Studio (Gemini 1.5 Flash)** para redactar guías de entrevista empática y preguntas abiertas para el tutor.
  * Detecta cortes de servicio y frena inferencias erróneas (Regla F1).
* **Lo que NO hace (Salvaguardas Éticas N1 a N4):**
  * **NUNCA contacta autónomamente a un estudiante:** La IA no envía correos, WhatsApps ni notificaciones directas al alumno.
  * **NUNCA sanciona ni da de baja:** No tiene permisos sobre el sistema de gestión académica (SIU Guaraní).
  * **NUNCA etiqueta de forma definitiva:** Las clasificaciones se recalculan cada 7 días; si el alumno recupera entregas, la alerta desaparece.
  * **NUNCA publica puntajes a docentes ni alumnos:** Solo los tutores asignados acceden a la bandeja de trabajo.

#### (d) Criterios de Éxito Medibles:
1. **Recall $\ge 70\%$:** Identificar al menos a 7 de cada 10 estudiantes que efectivamente abandonarían, con $\ge 4$ semanas de anticipación.
2. **Precisión $\ge 50\%$ en Nivel Alto:** Como máximo 1 de cada 2 alertas altas es un falso positivo.
3. **Equidad Algorítmica (Control de Sesgo):** Disparidad de recall entre turnos/comisiones (Mañana, Tarde, Noche) **$\le 10$ puntos porcentuales**.
4. **Validación de Hipótesis:** Reducción del **15% en el abandono** en el cuatrimestre piloto comparado contra el cuatrimestre previo.

---

### 3. CAPACIDAD DE IA Y VINCULACIÓN CON SUBCAMPOS

El sistema articula dos capacidades complementarias de Inteligencia Artificial:

1. **Clasificación y Aprendizaje Supervisado (Machine Learning / IA Simbólico-Conexionista):**
   * *Agente A2 (Evaluación de Riesgo):* Modelo de regresión logística multivariable calibrado con función sigmoide:
     $$P(\text{riesgo}) = \frac{1}{1 + e^{-z}}$$
     donde $z = \beta_0 + \sum \beta_i x_i$ pondera inasistencias acumuladas, ausencias recientes, TPs debidos, notas bajo el promedio y días de inactividad digital.
   * *Explicabilidad (XAI):* Descomposición de gradientes para extraer los 3 coeficientes con mayor peso relativo en el logit.

2. **Procesamiento de Lenguaje Natural (NLP) y Modelos de Lenguaje (LLMs):**
   * *Asistente Pedagógico con Google AI Studio (Gemini 1.5 Flash):* Generación de lenguaje natural condicionada por las variables del estudiante para producir guías de diálogo, preguntas socráticas y sugerencias pedagógicas sin sesgo punitivo.

---

### 4. FLUJO DE LA SOLUCIÓN: ENTRADAS ➔ PROCESAMIENTO (API) ➔ SALIDAS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. ENTRADAS (Fuentes semanales de datos crudos - Padrón 120 alumnos)        │
│   • Asistencia.csv (Docente / Secretaría Académica)                        │
│   • Notas.csv (Calificaciones Parcial 1 y TPs de cátedra)                   │
│   • Campus.csv (Logs de Moodle: último login, descargas, sesiones)          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. PROCESAMIENTO (Cadena Multiagente + API Gemini)                          │
│   • AGENTE A1 (Monitoreo): Valida esquemas, integra en 24h.                │
│     *Falla F1:* Si campus se corta, marca "Sin Evaluar" (Dato ≠ Inactividad)│
│   • AGENTE A2 (Inferencia ML): Scoring 0-100 + Top 3 factores XAI.          │
│   • AGENTE A3 (Priorización): Ordena, aplica tope (<=15) y regla F3.        │
│   • API GOOGLE AI STUDIO (Gemini 1.5 Flash):                                │
│     Prompt contextual ➔ Inferencia NLP ➔ Guía de entrevista personalizada. │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. SALIDAS (Bandeja del Tutor y Compuerta Humana N1-N4)                     │
│   • Bandeja de Alerta Temprana en Panel Web (UI Institucional).              │
│   • Ficha de Expediente Digital con explicabilidad gráfica de factores.     │
│   • Guía de preguntas empáticas generada por Gemini para la charla N2.      │
│   • Registro inmutable de decisión humana con hash de auditoría.            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 5. REQUISITOS MÍNIMOS, COSTOS Y SEGURIDAD

* **Datos Necesarios:** Registros de asistencia de secretaría, entregas en libretas de notas y logs de actividad virtual.
* **Costos de Infraestructura y Modelos:**
  * **$0 USD (Costo Cero):** El prototipo utiliza el **Free Tier de Google AI Studio** (Gemini 1.5 Flash permite hasta 15 solicitudes por minuto y 1.500 diarias gratuitas, suficiente para los 15 casos semanales por tutor).
  * Servidor local en Python estándar (`http.server` y `urllib`), sin costos de hosting ni base de datos cloud durante la fase experimental.
* **Seguridad y Privacidad (Punto N8):**
  * **Principio de Consentimiento:** Coordinación solo habilita fuentes de alumnos que hayan firmado el consentimiento informado de uso de datos educativos ($N8$).
  * **Aislamiento de Identidad en la API:** Los llamados a Google AI Studio no transmiten DNI, correos ni datos sensibles del alumno; solo variables académicas anónimas.
  * **Derecho de Acceso:** El estudiante puede solicitar formalmente ver qué variables suyas analiza el sistema.

---

### 6. ANÁLISIS ÉTICO: 5 RIESGOS OBLIGATORIOS Y MEDIDAS DE MITIGACIÓN

| # | Riesgo Ético Identificado | Impacto Potencial | Medida de Mitigación Implementada |
| :-: | :--- | :--- | :--- |
| **1** | **Sesgo Algorítmico (Equidad)** | Que el modelo prediga con menor precisión en el turno noche (donde los alumnos trabajan) que en la mañana. | **Métrica N7 en PEAS:** Se audita semestralmente que la diferencia de recall entre turnos sea $\le 10$ puntos. Si se supera, Coordinación bloquea el reentrenamiento. |
| **2** | **Vigilancia y Privacidad** | Sensación de invasión por el monitoreo de clics en el campus virtual. | **Punto N8:** Consentimiento explícito previo. Los datos son confidenciales y ningún puntaje se publica en listas abiertas. |
| **3** | **Uso Indebido y Estigmatización** | Que un profesor de aula califique con menor nota a un alumno sabiendo que la IA lo marcó en riesgo. | **Regla de Diseño C1:** La vista del docente de cátedra tiene **estrictamente bloqueados y ocultos los puntajes de riesgo**. El docente solo aporta datos. |
| **4** | **Dependencia Tecnológica (Falla de Sensores)** | Que una caída de Moodle por 48 h haga que la IA catalogue falsamente a todos los alumnos como desertores. | **Regla de Falla F1:** *La falta de dato NO se interpreta como inactividad*. El sistema suspende la puntuación y marca los casos como *«Sin Evaluar»*. |
| **5** | **Impacto Social (Deshumanización)** | Que se reemplace el vínculo pedagógico por correos automáticos amenazantes o impersonales. | **Compuerta Humana N1–N4:** El sistema no tiene actuadores directos hacia el estudiante. Todo contacto e intervención lo realiza un tutor de carne y hueso. |

---

### 7. GUION DE DEFENSA ORAL (5 MINUTOS CRONOMETRADOS)

* **0:00 – 0:45 | El Problema (Joel):**  
  *«En nuestra facultad el abandono se detecta cuando ya pasó: cuando el docente nota que un estudiante no viene, ya abandonó. El problema no es que nadie quiera ayudarlo, es que nadie se entera a tiempo. En Argentina solo 30 de cada 100 se reciben.»*
* **0:45 – 1:45 | La Solución y la Arquitectura (Joel):**  
  *«Proponemos SITA-IA: tres agentes en cadena. A1 consolida asistencia, notas y campus; A2 calcula el riesgo (0-100) y extrae los 3 motivos principales; A3 arma una lista corta con tope de 15 casos para no saturar al tutor. Es IA débil: alerta, no decide.»*
* **1:45 – 3:30 | Demostración en Vivo con Gemini API (Bautista y Joel):**  
  *«Mostramos el Caso Lucas González (82 puntos). A2 explica por qué: 40% de asistencia y 2 TPs pendientes. Conectamos la API de Gemini 1.5 Flash en Google AI Studio para que redacte una guía de diálogo empático con 3 preguntas abiertas para el tutor. Simulamos la Falla F1: si se corta el campus, el sistema congela el puntaje y marca 'Sin Evaluar' para no inventar datos.»*
* **3:30 – 4:15 | Compuerta Humana y Salvaguardas N1–N8 (Joel):**  
  *«El sistema se frena en la pantalla del tutor. Ningún agente le escribe al estudiante ni lo sanciona. Por la Regla C1, el docente de la materia no ve las alertas para no sesgar sus notas. Toda medida institucional (cambio de comisión) la aprueba Coordinación (N3).»*
* **4:15 – 5:00 | Límites, Sesgo y Recomendación Final (Bautista):**  
  *«El sistema solo observa rastros digitales y no las causas personales (trabajo, salud); eso lo descubre el tutor en la charla. Controlamos el sesgo con un límite de 10 puntos de diferencia entre turnos. Nuestra recomendación: la IA debe ser un radar preventivo que empodere el acompañamiento humano, nunca un tribunal que decida el futuro de un estudiante.»*
